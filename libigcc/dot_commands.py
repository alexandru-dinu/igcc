import source_code


class IGCCQuitException(Exception):
    pass


def dot_e(runner):
    print(runner.compile_error)
    return False, False


def dot_q(runner):
    raise IGCCQuitException()


def dot_l(runner):
    print("%s\n%s" % (runner.get_user_includes_string(), runner.get_user_commands_string()))
    return False, False


def dot_L(runner):
    print(source_code.get_full_source(runner))
    return False, False


def dot_r(runner):
    redone_line = runner.redo()
    if redone_line is not None:
        print("[Redone '%s'.]" % redone_line)
        return False, True
    else:
        print("[Nothing to redo.]")
        return False, False


def dot_u(runner):
    undone_line = runner.undo()
    if undone_line is not None:
        print("[Undone '%s'.]" % undone_line)
    else:
        print("[Nothing to undo.]")

    return False, False


def dot_h(runner):
    for cmd in sorted(dot_commands.keys()):
        print(cmd, dot_commands[cmd][0])

    return False, False


def process(inp, runner):
    if inp == ".h":
        return dot_h(runner)

    for cmd in sorted(dot_commands.keys()):
        if inp == cmd:
            return dot_commands[cmd][1](runner)

    return True, True


dot_commands = {
    ".e": ("Show the last compile errors/warnings", dot_e),
    ".h": ("Show this help message", None),
    ".q": ("Quit", dot_q),
    ".l": ("List the code you have entered", dot_l),
    ".L": ("List the whole program as given to the compiler", dot_L),
    ".r": ("Redo undone command", dot_r),
    ".u": ("Undo previous command", dot_u),
}
