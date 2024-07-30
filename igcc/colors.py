# https://stackoverflow.com/questions/9468435/how-to-fix-column-calculation-in-python-readline-if-using-color-prompt
COLORS = {
    "black": "\001\033[30m\002",
    "red": "\001\033[31m\002",
    "green": "\001\033[32m\002",
    "yellow": "\001\033[33m\002",
    "blue": "\001\033[34m\002",
    "magenta": "\001\033[35m\002",
    "cyan": "\001\033[36m\002",
    "white": "\001\033[37m\002",
    "reset": "\001\033[0m\002",
}


def colorize(xs, color):
    return f'{COLORS[color]}{xs}{COLORS["reset"]}'
