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

import source_code
import copying

class IGCCQuitException:
	pass

def dot_c( runner ):
	print copying.copying
	return False, False

def dot_e( runner ):
	print runner.compile_error,
	return False, False

def dot_q( runner ):
	raise IGCCQuitException()

def dot_l( runner ):
	print "%s\n%s" % ( runner.get_user_includes_string(), runner.get_user_commands_string() )
	return False, False

def dot_L( runner ):
	print source_code.get_full_source( runner )
	return False, False

def dot_r( runner ):
	redone_line = runner.redo()
	if redone_line is not None:
		print "[Redone '%s'.]" % redone_line
		return False, True
	else:
		print "[Nothing to redo.]"
		return False, False
		

def dot_u( runner ):
	undone_line = runner.undo()
	if undone_line is not None:
		print "[Undone '%s'.]" % undone_line
	else:
		print "[Nothing to undo.]"
	return False, False

def dot_w( runner ):
	print copying.warranty
	return False, False

dot_commands = {
	".c" : ( "Show copying information", dot_c ),
	".e" : ( "Show the last compile errors/warnings", dot_e ),
	".h" : ( "Show this help message", None ),
	".q" : ( "Quit", dot_q ),
	".l" : ( "List the code you have entered", dot_l ),
	".L" : ( "List the whole program as given to the compiler", dot_L ),
	".r" : ( "Redo undone command", dot_r ),
	".u" : ( "Undo previous command", dot_u ),
	".w" : ( "Show warranty information", dot_w ),
	}

def case_insensitive_string_compare( str1, str2 ):
	return cmp( str1.lower(), str2.lower() )

def dot_h( runner ):
	for cmd in sorted( dot_commands.keys(), case_insensitive_string_compare ):
		print cmd, dot_commands[cmd][0]
	return False, False

def process( inp, runner ):
	if inp == ".h":
		return dot_h( runner )

	for cmd in sorted( dot_commands.keys() ):
		if inp == cmd:
			return dot_commands[cmd][1]( runner )

	return True, True

