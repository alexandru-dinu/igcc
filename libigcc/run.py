# igcc - a read-eval-print loop for C/C++ programmers
#
# Copyright (C) 2009 Andy Balaam
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.

import code
import os
import os.path
import re
import subprocess
import sys
import tempfile
from optparse import OptionParser

import dot_commands
import source_code
import version

# --------------

prompt = "g++> "
compiler_command = ( "g++", "-x", "c++", "$include_dirs",
	"-o", "$outfile", "-" )

include_command = ( "-I", "$include_dir" )

incl_re = re.compile( r"\s*#\s*include\s" )

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

def get_compiler_command( options, outfilename ):
	ret = []
	for part in compiler_command:
		if part == "$include_dirs":
			if options.DIR is not None:
				for incl_dir in options.DIR:
					for incl_part in include_command:
						ret.append(
							incl_part.replace( "$include_dir" , incl_dir ) )
		else:
			ret.append( part.replace( "$outfile", outfilename ) )
	return ret


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

def print_welcome():
	print '''igcc $version
Released under GNU GPL version 2 or later, with NO WARRANTY.
Type ".h" for help.
'''.replace( "$version", version.VERSION )

def do_run( options, inputfile, exefilename ):
	read_line = create_read_line_function( inputfile, prompt )

	subs_compiler_command = get_compiler_command( options, exefilename )

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

def parse_args( argv ):
	parser = OptionParser( version="igcc " + version.VERSION )
			
	parser.add_option( "-I", "", dest="DIR", action="append",
		help = "Add the directory DIR to the list of directories to " +
			"be searched for header files." )
		
	(options, args) = parser.parse_args( argv )

	if len( args ) > 0:
		parser.error( "Unrecognised arguments :" +
			" ".join( arg for arg in args ) )

	return options

def run( outputfile = sys.stdout, inputfile = None, print_welc = True,
		argv = None ):

	# TODO: replace try...finally with a "with" statement
	real_sys_stdout = sys.stdout
	sys.stdout = outputfile

	exefilename = ""

	try:
		options = parse_args( argv )

		exefilename = get_temporary_file_name()
		ret = "normal"
		if print_welc:
			print_welcome()
		do_run( options, inputfile, exefilename )
	except dot_commands.IGCCQuitException:
		ret = "quit"
	finally:
		sys.stdout = real_sys_stdout

		if os.path.isfile( exefilename ):
			os.remove( exefilename )

	return ret

