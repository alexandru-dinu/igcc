#!/bin/bash

function test_lib_dir()
{
    cd cpp1 && \
    g++ -o mylib.o -c mylib.cpp && \
    ar rc libmylib.a mylib.o && \
    ranlib libmylib.a && \

    cd .. && \

    echo -e '#include "mylib.h"\ndefined_in_cpp();' | \
    python ../igcc -I../libigcc -Icpp1 -Lcpp1 -lmylib | \
    grep "defined_in_cpp saying hello" > /dev/null

    if [[ $? != 0 ]]; then
    {
        echo "test_lib_dir failed."
        exit 1
    }; fi
}

test_lib_dir && echo "Lib test passed." && rm -rf cpp1/*.a cpp1/*.o