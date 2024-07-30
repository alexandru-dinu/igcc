# Interactive GCC

[![workflow](https://github.com/alexandru-dinu/igcc/workflows/CI/badge.svg)](https://github.com/alexandru-dinu/igcc/actions?query=workflow%3ACI)
[![contrib](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/alexandru-dinu/igcc/issues)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**NOTE**: This is forked from https://sourceforge.net/projects/igcc/. I've done some refactoring and I'm currently maintaining it.

- Interactive GCC (igcc) is a read-eval-print loop (REPL) for C/C++
- A default [`boilerplate.h`](https://github.com/alexandru-dinu/igcc/blob/main/igcc/assets/boilerplate.h) header is included, with `<bits/stdc++.h>`, `using namespace std;`, and some helper functions
- For configuration (mainly related to compiling) see [`config.yaml`](https://github.com/alexandru-dinu/igcc/blob/main/igcc/assets/config.yaml)

## Running

Optionally, first create a new python virtual environment, then:
```bash
pip3 install git+https://github.com/alexandru-dinu/igcc.git
```
Now you can run the REPL with:
```
igcc
```
By default, the [`assets/`](https://github.com/alexandru-dinu/igcc/tree/main/igcc/assets) include dir will be available, exporting `boilerplate.h`.

For all available args, use: `igcc --help`.

The code will be compiled with GCC and the results (if any) will be displayed.
Type `.h` for help:

```
[  1] > .h
.L List the whole program as given to the compiler
.e Show the last compile errors/warnings
.h Show this help message
.l List the code you have entered
.q Quit
.r Redo undone command
.u Undo previous command
```

## Usage

Simple usage:

```
$ igcc
[  1] > int a = 5;
[  2] > a += 2;
[  3] > cout << a << endl;
7
[  4] > --a;
[  5] > cout << a << endl;
6
```

Include header files:

```
$ igcc
[  1] > #include <vector>
[  2] > vector<int> xs = {1,2,3};
[  3] > xs.push_back(17);
[  4] > xs.pop_back();
[  5] > printf("%u", xs.size());
3
```

Compile errors can be tolerated until the code works:

```
$ igcc
[  1] > for (int i = 0; i < 10; i++) {
Compile error - type .e to see it OR disregard if multi-line statement(s)

[  2] > cout << i << " ";
Compile error - type .e to see it OR disregard if multi-line statement(s)

[  3] > }
0 1 2 3 4 5 6 7 8 9
```

Libs can be linked:

```
$ igcc -lpthread
[  1] > #include <pthread.h>
[  2] > pthread_t thr;
[  3] > const char* msg = "Hello, World!";
[  4] > // assuming print_msg is defined somewhere
[  5] > int ret = pthread_create(&thr, NULL, print_msg, (void*) msg); pthread_join(thr, NULL);
Hello, World!
```

## Links
- [IGCC home page](http://www.artificialworlds.net/wiki/IGCC/IGCC)
- [IGCC Sourceforge page](http://sourceforge.net/projects/igcc/)
- [Andy Balaam's home page](http://www.artificialworlds.net)
- [Andy Balaam's blog](http://www.artificialworlds.net/blog)

## Credits

- Andy Balaam may be contacted on axis3x3 at users dot sourceforge dot net
- IGCC is Copyright (C) 2009 Andy Balaam
- IGCC is Free Software released under the terms of the GNU General Public License version 3
- IGCC comes with NO WARRANTY
