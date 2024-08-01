# Interactive GCC

[![tests](https://github.com/alexandru-dinu/igcc/actions/workflows/main.yml/badge.svg)](https://github.com/alexandru-dinu/igcc/actions/workflows/main.yml)
[![contrib](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/alexandru-dinu/igcc/issues)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> [!NOTE]
> The original repo from Andy Balaam is here: https://codeberg.org/andybalaam/igcc.
> In this fork, I've done some refactoring and tried to make it easier to use.

> [!WARNING]
> This project is a hacky attempt at getting a shorter feedback loop when working with C/C++ in some cases and it's obviously not intended for anything serious.

Interactive GCC (`igcc`) is a read-eval-print loop (REPL) for C/C++. It works by manipulating a base source file with user commands, compiles the source after each modification, then executes the resulting binary and collects its stdout & stderr.
Multi-line (block) input is supported, so you can add multiple lines in one go and invoke the compiler just once (examples below).

You can include various header files. For convenience, a default header is included: [`boilerplate.h`](https://github.com/alexandru-dinu/igcc/blob/main/igcc/assets/boilerplate.h). Also, `using namespace std;` is not available by default, but you can explicitly add it (example below).

Various aspects of `igcc` can be configured, see [`config.yaml`](https://github.com/alexandru-dinu/igcc/blob/main/igcc/assets/config.yaml).

## Getting started
The easiest way to get started is to use [pipx](https://pipx.pypa.io/stable/):
```
pipx install git+https://github.com/alexandru-dinu/igcc.git
```
Alternatively, you can also just use `pip` (a dedicated virtual environment is recommended).

Now you can run the REPL with:
```
igcc
```

Available args:
```
$ igcc --help
usage: igcc [-h] [-I INCLUDE [INCLUDE ...]] [-L LIBDIR [LIBDIR ...]] [-l LIB [LIB ...]]

options:
  -h, --help            show this help message and exit
  -I INCLUDE [INCLUDE ...]
                        Add INCLUDE to the list of directories to be searched for header files.
  -L LIBDIR [LIBDIR ...]
                        Add LIBDIR to the list of directories to be searched for library files.
  -l LIB [LIB ...]      Search the library LIB when linking.
```

The code will be compiled with GCC (`g++`) and the results (if any) will be displayed.
Type `.h` for help:

```
$ igcc
[1]> .h
.h  Show this help message
.e  Show the last compile errors/warnings
.l  List the code you have entered
.L  List the whole program as given to the compiler
.r  Redo undone command
.u  Undo previous command
.q  Quit
```

## Examples
```
$ igcc
[1]> int a = 5;
[2]> a += 2;
[3]> using namespace std;
[4]> cout << a << endl;
7

[5]> int b = 17;
[6]> a *= b;
[7]> cout << a << ", " << b << endl;
119, 17

[8]> .L
#include "boilerplate.h"
using namespace std;

int main(void) {
    int a = 5;
    a += 2;
    cout << a << endl;
    int b = 17;
    a *= b;
    cout << a << ", " << b << endl;

    return 0;
}
```

**Multi-line input** is supported (check `multiline_marker` from config). The benefit is avoiding multiple compiler calls.
```
$ igcc
[1]> .m
... for (int i = 0; i < 10; i++) {
...   std::cout << i << " ";
... }
... std::cout << "\n";
... .m
0 1 2 3 4 5 6 7 8 9
```

You can include headers:
```
$ igcc
[1]> #include <vector>
[2]> std::vector<int> xs{1,2,3};
[3]> xs.push_back(17);
[4]> .m
... for (auto x : xs) {
...   std::cout << x << " ";
... }
... .m
1 2 3 17
```

Libs can be linked:
```
$ igcc -lpthread
[  1]> #include <pthread.h>
[  2]> pthread_t thr;
[  3]> const char* msg = "Hello, World!";
[  4]> // assuming print_msg is defined somewhere
[  5]> int ret = pthread_create(&thr, NULL, print_msg, (void*) msg); pthread_join(thr, NULL);
Hello, World!
```

You can also **undo** commands:
```
$ igcc
[1]> int x = 2
 Compile error - type .e to see it

[2]> .e
<stdin>: In function ‘int main()’:
<stdin>:7:5: error: expected ‘,’ or ‘;’ before ‘return’
<stdin>:5:9: warning: unused variable ‘x’ [-Wunused-variable]

[2]> .u
Undone `int x = 2`
[1]> int x = 2;
[2]> .L
#include "boilerplate.h"


int main(void) {
    int x = 2;

    return 0;
}
```

... or **redo** previously undone commands:
```
$ igcc
[1]> int x = 2;
[2]> std::cout << x;
2
[3]> .u
Undone `std::cout << x;`
[2]> .L
#include "boilerplate.h"


int main(void) {
    int x = 2;

    return 0;
}
[2]> .r
Redone `std::cout << x;`
2
[3]> .L
#include "boilerplate.h"


int main(void) {
    int x = 2;
    std::cout << x;

    return 0;
}
```

## Future work
See https://github.com/alexandru-dinu/igcc/issues

## Similar projects
- https://github.com/BenBrock/reple: "Replay-based" REPLs for compiled languages
- https://github.com/root-project/cling: The cling C++ interpreter


## Credits
- [IGCC home page](http://www.artificialworlds.net/wiki/IGCC/IGCC)
- [IGCC Sourceforge page](http://sourceforge.net/projects/igcc/)
- [Andy Balaam's home page](http://www.artificialworlds.net)
- [Andy Balaam's blog](http://www.artificialworlds.net/blog)
- Andy Balaam may be contacted on axis3x3 at users dot sourceforge dot net
- IGCC is Copyright (C) 2009 Andy Balaam
- IGCC is Free Software released under the terms of the GNU General Public License version 3
- IGCC comes with NO WARRANTY
