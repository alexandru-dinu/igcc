#!/usr/bin/env bash

IGCC="igcc"

function test_lib_dir() {
	# make static lib
	g++ -o mylib.o -c mylib.cpp &&
		ar rc libmylib.a mylib.o &&
		ranlib libmylib.a

	# call 'defined_in_cpp()' function
	echo -e '#include "mylib.h"\ndefined_in_cpp();' |
		$IGCC -I. -L. -lmylib |
		grep "defined_in_cpp saying hello" >/dev/null

	if [[ $? != 0 ]]; then
		echo "test_lib_dir failed."
		exit 1
	fi
}

test_lib_dir && echo "test_lib_dir passed." && rm -rf *.a *.o
