#!/usr/bin/python

import code
import os
import os.path
import subprocess
import sys
import tempfile

# --------------

prompt = "g++> "
compiler_command = ( "g++", "-x", "c++", "-o", "$outfile", "-" )
file_boilerplate = """

#include "stdio.h"

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
		sys.stdout.write( line )
		#print line,
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

def run_compile( subs_compiler_command, user_commands ):
	compile_process = subprocess.Popen( subs_compiler_command,
		stdin = subprocess.PIPE )
	compile_process.communicate( file_boilerplate.replace(
		"$user_commands", user_commands ) )

def run_exe( exefilename ):
	run_process = subprocess.Popen( exefilename, stdout = subprocess.PIPE )
	return run_process.communicate()

def do_run( inputfile, exefilename ):
	read_line = create_read_line_function( inputfile, prompt )

	subs_compiler_command = get_compiler_command( exefilename )

	inp = 1
	user_commands = ""
	while inp is not None:
		inp = read_line()
		if inp is not None:
			user_commands += inp

			run_compile( subs_compiler_command, user_commands )
			stdoutdata, stderrdata = run_exe( exefilename )

			if len( stdoutdata ) > 0:
				print stdoutdata,

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


