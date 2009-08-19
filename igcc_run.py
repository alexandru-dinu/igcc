#!/usr/bin/python

import code
import os
import os.path
import re
import subprocess
import sys
import tempfile

# --------------

prompt = "g++> "
compiler_command = ( "g++", "-x", "c++", "-o", "$outfile", "-" )

incl_re = re.compile( r"\s*#include\s" )

file_boilerplate = """

#include <cstdio>
#include <iostream>
#include <string>

$user_includes

using namespace std;

int main( char*& argv, int argc )
{
	$user_commands
}
"""

#---------------


def read_line_from_stdin( ic, prompt ):
	try:
		return ic.raw_input( prompt )
	except EOFError:
		return None

def read_line_from_file( inputfile, prompt ):
	sys.stdout.write( prompt )
	line = inputfile.readline()
	if line is not None:
		print line
	return line

def create_read_line_function( inputfile, prompt ):
	if inputfile is None:
		ic = code.InteractiveConsole()
		return lambda: read_line_from_stdin( ic, prompt )
	else:
		return lambda: read_line_from_file( inputfile, prompt )

def get_temporary_file_name():
	outfile = tempfile.NamedTemporaryFile( prefix = 'igcc-exe' )
	outfilename = outfile.name
	outfile.close()
	return outfilename

def get_compiler_command( outfilename ):
	return tuple( part.replace( "$outfile", outfilename ) for
		part in compiler_command )

def get_full_source( user_commands, user_includes ):
	return ( file_boilerplate
		.replace( "$user_commands", user_commands )
		.replace( "$user_includes", user_includes )
		)

def run_compile( subs_compiler_command, user_commands, user_includes ):
	compile_process = subprocess.Popen( subs_compiler_command,
		stdin = subprocess.PIPE, stderr = subprocess.PIPE )
	stdoutdata, stderrdata = compile_process.communicate(
		get_full_source( user_commands, user_includes ) )

	if compile_process.returncode == 0:
		return None
	elif stdoutdata is not None:
		if stderrdata is not None:
			return stdoutdata + stderrdata
		else:
			return stdoutdata
	else:
		if stderrdata is not None:
			return stderrdata
		else:
			return "Unknown compile error - compiler did not write any output."
		

def run_exe( exefilename ):
	run_process = subprocess.Popen( exefilename, stdout = subprocess.PIPE )
	return run_process.communicate()

def do_run( inputfile, exefilename ):
	read_line = create_read_line_function( inputfile, prompt )

	subs_compiler_command = get_compiler_command( exefilename )

	inp = 1
	user_commands = ""
	user_includes = ""
	compile_error = ""
	output_chars_printed = 0
	while inp is not None:
		inp = read_line()
		if inp is not None:

			if inp == ".e":
				print compile_error,
			else:
				if incl_re.match( inp ):
					user_includes += inp
				else:
					user_commands += inp

				compile_error = run_compile( subs_compiler_command,
					user_commands, user_includes )
	
				if compile_error is not None:
					#print compile_error
					print "[Compile error - type .e to see it.]"
				else:
					stdoutdata, stderrdata = run_exe( exefilename )
		
					if len( stdoutdata ) > output_chars_printed:
						new_output = stdoutdata[output_chars_printed:]
						print new_output,
						output_chars_printed += len( new_output )

	print

def run( outputfile = sys.stdout, inputfile = None ):

	# TODO: replace try...finally with a "with" statement
	real_sys_stdout = sys.stdout
	sys.stdout = outputfile

	exefilename = get_temporary_file_name()

	try:
		do_run( inputfile, exefilename )
	finally:
		sys.stdout = real_sys_stdout

		if os.path.isfile( exefilename ):
			os.remove( exefilename )


