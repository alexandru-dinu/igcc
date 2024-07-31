import argparse
import tempfile
from importlib import resources
from pathlib import Path


def parse_args(argv) -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-I",
        nargs="+",
        dest="INCLUDE",
        help="Add INCLUDE to the list of directories to be searched for header files.",
        default=[],
    )
    parser.add_argument(
        "-L",
        nargs="+",
        dest="LIBDIR",
        help="Add LIBDIR to the list of directories to be searched for library files.",
    )
    parser.add_argument(
        "-l",
        nargs="+",
        dest="LIB",
        help="Search the library LIB when linking.",
    )

    args = parser.parse_args(argv)

    # make default asset dir available as include dir, as it defines `boilerplate.h`
    args.INCLUDE.insert(0, str(get_asset_dir()))

    return args


def get_asset_dir() -> Path:
    return resources.files("igcc").joinpath("assets")


def get_tmp_filename() -> Path:
    outfile = tempfile.NamedTemporaryFile(prefix="igcc-tmp")
    outfilename = outfile.name
    outfile.close()
    return Path(outfilename)


def read_from_stdin(prompt: str, n: int, multiline_marker: str = ".m") -> list[str] | None:
    try:
        first = input(f"[{n}]{prompt}").rstrip()

        # not multiline input
        if first != multiline_marker:
            return [first]

        # start multiline input
        ret = []
        while True:
            if (line := input("... ")) == multiline_marker:
                break
            ret.append(line)

        return ret

    except EOFError:
        return None


# TODO: rename
def append_multiple(single_cmd, cmdlist) -> list:
    if cmdlist is None:
        return []

    return [cmd_part.replace("$cmd", cmd) for cmd_part in single_cmd for cmd in cmdlist]


def get_compiler_command(config, args, out_filename) -> list[str]:
    ret = []

    for part in config.compiler_cmd.split():
        match part:
            case "$include_dirs":
                ret += append_multiple(config.include_dir_cmd.split(), args.INCLUDE)
            case "$lib_dirs":
                ret += append_multiple(config.lib_dir_cmd.split(), args.LIBDIR)
            case "$libs":
                ret += append_multiple(config.lib_cmd.split(), args.LIB)
            case _:
                ret.append(part.replace("$outfile", out_filename))

    return ret
