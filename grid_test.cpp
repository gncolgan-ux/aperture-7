#include <iostream>
#include <cmath>

int main() {
    double pi = std::acos(-1.0);
    std::cout << "[APERTURE CLOUD C++ CORE ONLINE]\n";
    for (int i = 0; i < 6; ++i) {
        std::cout << "Edge_" << i << " Phase Lock: " << ((i + 1) * pi / 3.0) << " rad\n";
    }
    return 0;
}
