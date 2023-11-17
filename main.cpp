//
// Created by anthony on 11/16/23.
//

#include <fstream>

#include "Cache.h"
#include "LRUPolicy.h"
#include "FIFOPolicy.h"

int main() {
    Cache<FIFOPolicy> cache(9, 6, 1);

    std::ifstream trace("../gcc.trace");

    if (!trace.is_open()) {
        return 1;
    }

    std::string address, _;
    unsigned int hits = 0, count = 0;

    while (!trace.eof()) {
        getline(trace, _, ' ');
        getline(trace, address, ' ');
        getline(trace, _);

        if (address.length() == 0) {
            continue;
        }

        unsigned int addr = std::stol(address, nullptr, 16);

        hits += cache.check_cache(addr) ? 1 : 0;
        ++count;
    }

    double hit_rate = (double) hits / count;
    std::cout << "Hits " << hits << " accesses " << count << " hit rate " << hit_rate << '\n';

    return 0;
}