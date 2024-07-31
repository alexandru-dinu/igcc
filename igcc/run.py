import argparse
import itertools
import re
import readline
import subprocess
import sys
from dataclasses import dataclass

import yaml
from rich import print

import igcc.utils

readline.parse_and_bind("tab: complete")


with open(igcc.utils.get_asset_dir() / "config.yaml") as fp:
    CONFIG = argparse.Namespace(**yaml.safe_load(fp))

INCL_RE = re.compile(r"\s*#\s*include\s")

SOURCE_CODE = """
#include "boilerplate.h"
$user_includes
int main(void) {
    $user_input
    return 0;
}
""".strip()


class IGCCQuitException(Exception):
    pass


@dataclass
class UserInput:
    inp: str
    is_include: bool
    output_chars: int = 0
    error_chars: int = 0


class Runner:
    def __init__(self, args, input_file, exec_filename):
        self.args = args
        self.input_file = input_file
        self.exec_filename = str(exec_filename)
        self.user_input = []
        self.input_num = 0
        self.compile_error = ""
        self.output_chars_printed = 0
        self.error_chars_printed = 0
        self.subs_compiler_cmd = igcc.utils.get_compiler_command(
            CONFIG, self.args, self.exec_filename
        )

    def do_run(self):
        while True:
            inp = igcc.utils.read_from_stdin(
                CONFIG.prompt, self.input_num + 1, CONFIG.multiline_marker
            )
            if inp is None:
                break

            # input is joined when sent to the compiler
            # to avoid repeated calls to the compiler for multiline
            # however, each line (UserInput) is accounted for separately
            col_inp, run_compiler = self.process("\n".join(inp))

            if col_inp:
                if self.input_num < len(self.user_input):
                    self.user_input = self.user_input[: self.input_num]

                new_inp = [UserInput(x, is_include=INCL_RE.match(x) is not None) for x in inp]
                self.user_input += new_inp
                self.input_num += len(new_inp)

            if run_compiler:
                self.compile_error = self.run_compile()

                if self.compile_error is not None:
                    print("[red] Compile error - type .e to see it\n [/red]")
                    continue

                # execute the compiled binary
                stdout_data, stderr_data = igcc.utils.run_exec(self.exec_filename)

                if len(stdout_data) > self.output_chars_printed:
                    new_output = stdout_data[self.output_chars_printed :]
                    len_new_output = len(new_output)

                    print(new_output.decode("utf8"))

                    self.output_chars_printed += len_new_output
                    self.user_input[-1].output_chars = len_new_output

                if len(stderr_data) > self.error_chars_printed:
                    new_error = stderr_data[self.error_chars_printed :]
                    len_new_error = len(new_error)

                    print(new_error.decode("utf8"))

                    self.error_chars_printed += len_new_error
                    self.user_input[-1].error_chars = len_new_error

    def redo(self):
        if self.input_num >= len(self.user_input):
            return None

        self.input_num += 1
        return self.user_input[self.input_num - 1].inp

    def undo(self):
        if self.input_num == 0:
            return None

        self.input_num -= 1
        undone_input = self.user_input[self.input_num]
        self.output_chars_printed -= undone_input.output_chars
        self.error_chars_printed -= undone_input.error_chars

        return undone_input.inp

    def get_full_source(self):
        return SOURCE_CODE.replace("$user_input", self.get_user_commands_string()).replace(
            "$user_includes", self.get_user_includes_string()
        )

    def get_user_input(self):
        return itertools.islice(self.user_input, 0, self.input_num)

    def get_user_commands_string(self):
        user_cmds = (a.inp for a in filter(lambda a: not a.is_include, self.get_user_input()))
        return "\n".join(user_cmds) + "\n"

    def get_user_includes_string(self):
        user_includes = (a.inp for a in filter(lambda a: a.is_include, self.get_user_input()))
        return "\n".join(user_includes) + "\n"

    def run_compile(self):
        src = self.get_full_source()

        compile_process = subprocess.Popen(
            self.subs_compiler_cmd,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf8",
        )

        stdout_data, stderr_data = compile_process.communicate(input=src)

        if compile_process.returncode == 0:
            return None

        out = ""

        if stdout_data is not None:
            out += stdout_data

        if stderr_data is not None:
            out += stderr_data

        if out == "":
            return "Unknown compile error - compiler did not write any output."

        return out

    # DOT COMMANDS
    # TODO: maybe extract separately or make the return values more explicit

    def process(self, inp):
        r = self.dot_commands.get(inp)

        if r is not None:
            desc, func = r
            return func(self)

        return True, True

    def dot_e(self):
        print(self.compile_error)
        return False, False

    def dot_q(self):
        raise IGCCQuitException()

    def dot_l(self):
        print(f"{self.get_user_includes_string()}\n{self.get_user_commands_string()}")
        return False, False

    def dot_L(self):
        print(self.get_full_source())
        return False, False

    def dot_r(self):
        redone_line = self.redo()
        if redone_line is not None:
            print(f"Redone [{redone_line}]")
            return False, True
        else:
            print("Nothing to redo")
            return False, False

    def dot_u(self):
        undone_line = self.undo()
        if undone_line is not None:
            print(f"Undone [{undone_line}]")
        else:
            print("Nothing to undo")

        return False, False

    def dot_h(self):
        for cmd in sorted(self.dot_commands.keys()):
            print(cmd, self.dot_commands[cmd][0])

        return False, False

    dot_commands = {
        ".h": ("Show this help message", dot_h),
        ".e": ("Show the last compile errors/warnings", dot_e),
        ".l": ("List the code you have entered", dot_l),
        ".L": ("List the whole program as given to the compiler", dot_L),
        ".r": ("Redo undone command", dot_r),
        ".u": ("Undo previous command", dot_u),
        ".q": ("Quit", dot_q),
    }


# ENTRYPOINT
def repl() -> None:
    exec_filename = None

    try:
        try:
            args = igcc.utils.parse_args(sys.argv[1:])
            exec_filename = igcc.utils.get_tmp_filename()
            Runner(args, input_file=None, exec_filename=exec_filename).do_run()
        except (IGCCQuitException, KeyboardInterrupt):
            pass

    finally:
        if exec_filename is not None and exec_filename.exists():
            exec_filename.unlink()
