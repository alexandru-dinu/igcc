import code
import os
import os.path
import re
import subprocess
import sys
import tempfile

import dot_commands
import source_code

# --------------

prompt = "g++> "
compiler_command = ( "g++", "-x", "c++", "-o", "$outfile", "-" )

incl_re = re.compile( r"\s*#include\s" )

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


def run_compile( subs_compiler_command, user_commands, user_includes ):
	compile_process = subprocess.Popen( subs_compiler_command,
		stdin = subprocess.PIPE, stderr = subprocess.PIPE )
	stdoutdata, stderrdata = compile_process.communicate(
		source_code.get_full_source( user_commands, user_includes ) )

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

			if not dot_commands.process( inp, user_commands, user_includes,
					compile_error ):
				if incl_re.match( inp ):
					user_includes += inp + "\n"
				else:
					user_commands += inp + "\n"

				compile_error = run_compile( subs_compiler_command,
					user_commands, user_includes )
	
				if compile_error is not None:
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


