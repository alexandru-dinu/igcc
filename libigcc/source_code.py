file_boilerplate = """
#include <cstdio>
#include <iostream>
#include <string>

$user_includes

using namespace std;

int main(void)
{
    $user_commands
    
    return 0;
}
"""


def get_full_source(runner):
    return (file_boilerplate
            .replace("$user_commands", runner.get_user_commands_string())
            .replace("$user_includes", runner.get_user_includes_string())
            )
