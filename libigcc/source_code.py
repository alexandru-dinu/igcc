
file_boilerplate = """#include <cstdio>
#include <iostream>
#include <string>
$user_includes
using namespace std;

int main()
{
	$user_commands
}
"""


def get_full_source( user_commands, user_includes ):
	return ( file_boilerplate
		.replace( "$user_commands", user_commands )
		.replace( "$user_includes", user_includes )
		)

