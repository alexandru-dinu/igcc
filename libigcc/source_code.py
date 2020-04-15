file_boilerplate = """
#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <sstream>
#include <queue>
#include <deque>
#include <bitset>
#include <iterator>
#include <list>
#include <stack>
#include <map>
#include <unordered_map>
#include <set>
#include <unordered_set>
#include <functional>
#include <numeric>
#include <utility>
#include <limits>
#include <time.h>
#include <math.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <assert.h>

$user_includes

using namespace std;

int main(void)
{
    $user_input

    return 0;
}
""".strip()


def get_full_source(runner):
    return (file_boilerplate
            .replace("$user_input", runner.get_user_commands_string())
            .replace("$user_includes", runner.get_user_includes_string()))
