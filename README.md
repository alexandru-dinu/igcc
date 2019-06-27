# Interactive GCC

_This is forked from https://sourceforge.net/projects/igcc/. I have done some refactoring and ported to Python 3.7, currently maintaining it._

Interactive GCC (igcc) is a read-eval-print loop (REPL) for C/C++ programmers.
The `cstdio`, `iostream` and `string` headers are automatically included,
and the `std namespace` is automatically in scope.

It can be used like this:

```
$ ./igcc
g++> int a = 5;
g++> a += 2;
g++> cout << a << endl;
7
g++> --a;
g++> cout << a << endl;
6
g++>
```

It is possible to include header files you need like this:

```
$ ./igcc
g++> #include <vector>
g++> vector<int> myvec;
g++> myvec.push_back( 17 );
g++> printf( "%d\n", myvec.size() );
1
g++> myvec.push_back( 21 );
g++> printf( "%d\n", myvec.size() );
2
g++>
```

Compile errors can be tolerated until the code works:

```
$ ./igcc
g++> #include <map>
g++> map<string,int> hits;
g++> hits["foo"] = 12;
g++> hits["bar"] = 15;
g++> for( map<string,int>::iterator it = hits.begin(); it != hits.end(); ++it )
[Compile error - type .e to see it.]
g++> {
[Compile error - type .e to see it.]
g++> 	cout << it->first << " " << it->second << endl;
[Compile error - type .e to see it.]
g++> }
bar 15
foo 12
g++>
```

Extra include directories can be supplied:

```
$ ./igcc -Itest/cpp -Itest/cpp2
g++> #include "hello.h"
g++> hello();
Hello,
g++> #include "world.h"
g++> world();
world!
g++>
```

Libs can be linked:

```
$ ./igcc -lm
g++> #include "math.h"
g++> cout << pow( 3, 3 ) << endl; // Actually a bad example since libm.a is already linked in C++
27
g++>
```

Your own libs can be linked too:

```
$ ./igcc -Itest/cpp -Ltest/cpp -lmylib
g++> #include "mylib.h"
g++> defined_in_cpp();
defined_in_cpp saying hello.
g++>
```

## Downloading and usage

Clone the repository, then run the prompt:
```
./igcc
```

The code will be compiled with GCC and the results (if any) will be displayed.
Type `.h` to see some (minimal) help.


## Links
- [IGCC home page](http://www.artificialworlds.net/wiki/IGCC/IGCC)
- [IGCC Sourceforge page](http://sourceforge.net/projects/igcc/)
- [Andy Balaam's home page](http://www.artificialworlds.net)
- [Andy Balaam's blog](http://www.artificialworlds.net/blog)

## Credits

Andy Balaam may be contacted on axis3x3 at users dot sourceforge dot net

IGCC is Copyright (C) 2009 Andy Balaam

IGCC is Free Software released under the terms of the GNU General Public License version 2 or later.

IGCC comes with NO WARRANTY.

See the file COPYING for more information.
