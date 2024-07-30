source_code = """
#include "boilerplate.h"

$user_includes

int main(void) {
    $user_input

    return 0;
}
""".strip()


def get_full_source(runner):
    return source_code.replace("$user_input", runner.get_user_commands_string()).replace(
        "$user_includes", runner.get_user_includes_string()
    )
