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

def dot_c( user_commands, user_includes, compile_error ):
	print copying.copying

def dot_e( user_commands, user_includes, compile_error ):
	print compile_error,

def dot_q( user_commands, user_includes, compile_error ):
	raise IGCCQuitException()

def dot_l( user_commands, user_includes, compile_error ):
	print "%s\n%s" % ( user_includes, user_commands )

def dot_L( user_commands, user_includes, compile_error ):
	print source_code.get_full_source( user_commands, user_includes )

def dot_w( user_commands, user_includes, compile_error ):
	print copying.warranty

dot_commands = {
	".c" : ( "Show copying information", dot_c ),
	".e" : ( "Show the last compile errors/warnings", dot_e ),
	".h" : ( "Show this help message", None ),
	".q" : ( "Quit", dot_q ),
	".l" : ( "List the code you have entered", dot_l ),
	".L" : ( "List the whole program as given to the compiler", dot_L ),
	".w" : ( "Show warranty information", dot_w ),
	}

def case_insensitive_string_compare( str1, str2 ):
	return cmp( str1.lower(), str2.lower() )

def dot_h(  user_commands, user_includes, compile_error ):
	for cmd in sorted( dot_commands.keys(), case_insensitive_string_compare ):
		print cmd, dot_commands[cmd][0]

def process( inp, user_commands, user_includes, compile_error ):
	if inp == ".h":
		dot_h( user_commands, user_includes, compile_error )
		return True

	for cmd in sorted( dot_commands.keys() ):
		if inp == cmd:
			dot_commands[cmd][1]( user_commands, user_includes, compile_error )
			return True

	return False

