import argparse
import itertools
import os
import os.path
import re
import readline
import subprocess
import sys
import tempfile
from optparse import OptionParser

import yaml

import dot_commands
import source_code
from colors import colorize

readline.parse_and_bind('tab: complete')

config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../config/config.yaml')
config = argparse.Namespace(**yaml.safe_load(open(config_path)))

incl_re = re.compile(r"\s*#\s*include\s")

def read_line_from_stdin(prompt, n):
    prompt = colorize(f'[{n:3d}] {prompt}', 'green')
    try:
        return input(prompt).rstrip()
    except EOFError:
        return None

def read_line_from_file(input_file, prompt, n):
    prompt = colorize(f'[{n:3d}] {prompt}', 'green')
    sys.stdout.write(prompt)
    line = input_file.readline()

    if line is not None:
        print(line)

    return line

def create_read_line_function(input_file, prompt):
    if input_file is None:
        return lambda n: read_line_from_stdin(prompt, n)
    else:
        return lambda n: read_line_from_file(input_file, prompt, n)

def get_tmp_filename():
    outfile = tempfile.NamedTemporaryFile(prefix='igcc-tmp')
    outfilename = outfile.name
    outfile.close()
    return outfilename

def append_multiple(single_cmd, cmdlist, ret):
    if cmdlist is not None:
        ret += [cmd_part.replace("$cmd", cmd) for cmd_part in single_cmd for cmd in cmdlist]

def get_compiler_command(options, out_filename):
    ret = []

    for part in config.compiler_cmd.split():
        if part == "$include_dirs":
            append_multiple(config.include_dir_cmd.split(), options.INCLUDE, ret)
        elif part == "$lib_dirs":
            append_multiple(config.lib_dir_cmd.split(), options.LIBDIR, ret)
        elif part == "$libs":
            append_multiple(config.lib_cmd.split(), options.LIB, ret)
        else:
            ret.append(part.replace("$outfile", out_filename))

    return ret

def run_compile(subs_compiler_command, runner):
    src = source_code.get_full_source(runner)

    compile_process = subprocess.Popen(
        subs_compiler_command,
        stdin=subprocess.PIPE, stderr=subprocess.PIPE,
        encoding='utf8')

    stdout_data, stderr_data = compile_process.communicate(input=src)

    if compile_process.returncode == 0:
        return None

    out = ''

    if stdout_data is not None:
        out += stdout_data

    if stderr_data is not None:
        out += stderr_data

    if out == '':
        return "Unknown compile error - compiler did not write any output."

    return out

def run_exec(file_name):
    return subprocess.Popen(file_name,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE).communicate()

class UserInput:
    INCLUDE = 0
    COMMAND = 1

    def __init__(self, inp, typ):
        self.inp = inp
        self.typ = typ
        self.output_chars = 0
        self.error_chars = 0

    def __str__(self):
        return f"UserInput( {self.inp}, {self.typ}, {self.output_chars}, {self.error_chars} )"

    def __eq__(self, other):
        return all([
            self.inp == other.inp,
            self.typ == other.typ,
            self.output_chars == other.output_chars,
            self.error_chars == other.error_chars,
        ])

    def __ne__(self, other):
        return not self.__eq__(other)

class Runner:
    def __init__(self, options, input_file, exec_filename):
        self.options = options
        self.input_file = input_file
        self.exec_filename = exec_filename
        self.user_input = []
        self.input_num = 0
        self.compile_error = ""
        self.output_chars_printed = 0
        self.error_chars_printed = 0

    def do_run(self):
        read_line = create_read_line_function(self.input_file, config.prompt)
        subs_compiler_command = get_compiler_command(self.options, self.exec_filename)

        while True:
            inp = read_line(self.input_num)
            if inp is None:
                break

            col_inp, run_compiler = dot_commands.process(inp, self)

            if col_inp:
                if self.input_num < len(self.user_input):
                    self.user_input = self.user_input[: self.input_num]

                typ = [UserInput.COMMAND, UserInput.INCLUDE][incl_re.match(inp) is not None]
                self.user_input.append(UserInput(inp, typ))
                self.input_num += 1

            if run_compiler:
                self.compile_error = run_compile(subs_compiler_command, self)

                if self.compile_error is not None:
                    info = 'Compile error - type .e to see it OR disregard if multi-line statement(s)\n'
                    print(colorize(info, 'magenta'))
                    continue

                stdout_data, stderr_data = run_exec(self.exec_filename)

                if len(stdout_data) > self.output_chars_printed:
                    new_output = stdout_data[self.output_chars_printed:]
                    len_new_output = len(new_output)

                    print(new_output.decode('utf8'))

                    self.output_chars_printed += len_new_output
                    self.user_input[-1].output_chars = len_new_output

                if len(stderr_data) > self.error_chars_printed:
                    new_error = stderr_data[self.error_chars_printed:]
                    len_new_error = len(new_error)

                    print(new_error.decode('utf8'))

                    self.error_chars_printed += len_new_error
                    self.user_input[-1].error_chars = len_new_error

            print()  # ensure empty newline between commands

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

    def get_user_input(self):
        return itertools.islice(self.user_input, 0, self.input_num)

    def get_user_commands(self):
        return (a.inp for a in filter(lambda a: a.typ == UserInput.COMMAND, self.get_user_input()))

    def get_user_includes(self):
        return (a.inp for a in filter(lambda a: a.typ == UserInput.INCLUDE, self.get_user_input()))

    def get_user_commands_string(self):
        return "\n".join(self.get_user_commands()) + "\n"

    def get_user_includes_string(self):
        return "\n".join(self.get_user_includes()) + "\n"

def parse_args(argv):
    parser = OptionParser()

    parser.add_option("-I", "", dest="INCLUDE", action="append",
        help="Add INCLUDE to the list of directories to " +
             "be searched for header files.")
    parser.add_option("-L", "", dest="LIBDIR", action="append",
        help="Add LIBDIR to the list of directories to " +
             "be searched for library files.")
    parser.add_option("-l", "", dest="LIB", action="append",
        help="Search the library LIB when linking.")

    options, args = parser.parse_args(argv)

    if len(args) > 0:
        parser.error("Unrecognised arguments :" + " ".join(arg for arg in args))

    return options

def run(output_file=sys.stdout, input_file=None, argv=None):
    real_sys_stdout = sys.stdout
    sys.stdout = output_file
    exec_filename = ""

    try:
        try:
            options = parse_args(argv)

            exec_filename = get_tmp_filename()
            ret = "normal"

            Runner(options, input_file, exec_filename).do_run()

        except (dot_commands.IGCCQuitException, KeyboardInterrupt):
            ret = "quit"

    finally:
        sys.stdout = real_sys_stdout

        if os.path.isfile(exec_filename):
            os.remove(exec_filename)

    return ret
