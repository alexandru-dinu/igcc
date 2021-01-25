# Interactive GCC

[![workflow](https://github.com/alexandru-dinu/igcc/workflows/CI/badge.svg)](https://github.com/alexandru-dinu/igcc/actions?query=workflow%3ACI)
[![contrib](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/alexandru-dinu/igcc/issues)
[![gitpod](https://img.shields.io/badge/Gitpod-Ready--to--Code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/alexandru-dinu/igcc)

**NOTE**: This is forked from https://sourceforge.net/projects/igcc/. I have done some refactoring and ported it to Python 3.7. I am currently maintaining it.

- Interactive GCC (igcc) is a read-eval-print loop (REPL) for C/C++
- A default [`libigcc/boilerplate.h`](https://github.com/alexandru-dinu/igcc/blob/master/libigcc/boilerplate.h) header is included, with `<bits/stdc++.h>`, `using namespace std;`, and some helper functions
- For configuration (mainly related to compiling) see [`config/config.yaml`](https://github.com/alexandru-dinu/igcc/blob/master/config/config.yaml)

## Running

```bash
git clone https://github.com/alexandru-dinu/igcc.git
cd igcc
pip install -r requirements.txt
./igcc -I libigcc
```

The code will be compiled with GCC and the results (if any) will be displayed.
Type `.h` for help:

```
[  1] igcc> .h
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
$ ./igcc -I libigcc
[  1] igcc> int a = 5;
[  2] igcc> a += 2;
[  3] igcc> cout << a << endl;
7
[  4] igcc> --a;
[  5] igcc> cout << a << endl;
6
```

Include header files:

```
$ ./igcc -I libigcc
[  1] igcc> #include <vector>
[  2] igcc> vector<int> xs = {1,2,3};
[  3] igcc> xs.push_back(17);
[  4] igcc> xs.pop_back();
[  5] igcc> printf("%u", xs.size());
3
```

Compile errors can be tolerated until the code works:

```
$ ./igcc
[  1] igcc> for (int i = 0; i < 10; i++) {
Compile error - type .e to see it OR disregard if multi-line statement(s)

[  2] igcc> cout << i << " ";
Compile error - type .e to see it OR disregard if multi-line statement(s)

[  3] igcc> }
0 1 2 3 4 5 6 7 8 9
```

Libs can be linked:

```
$ ./igcc -I libigcc -lpthread
[  1] igcc> #include <pthread.h>
[  2] igcc> pthread_t thr;
[  3] igcc> const char* msg = "Hello, World!";
[  4] igcc> // assuming print_msg is defined somewhere
[  5] igcc> int ret = pthread_create(&thr, NULL, print_msg, (void*) msg); pthread_join(thr, NULL);
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
