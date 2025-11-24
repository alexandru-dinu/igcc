#include <iostream>
#include <vector>

template <typename T>
void print_vector(const std::vector<T>& xs) {
    for (const T& x : xs)
        std::cout << x << std::endl;
}
