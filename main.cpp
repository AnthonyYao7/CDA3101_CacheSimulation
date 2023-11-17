//
// Created by anthony on 11/16/23.
//

#include <fstream>
#include <sstream>

#include "Cache.h"
#include "LRUPolicy.h"
#include "FIFOPolicy.h"

struct CacheTestResult {
    unsigned int hits{};
    unsigned int accesses{};
};

CacheTestResult test_cache(unsigned int cache_size_log2, unsigned int line_size_log2, unsigned int set_size_log2, const std::string& filename) {
    Cache<FIFOPolicy> cache(cache_size_log2, line_size_log2, set_size_log2);

    std::ifstream trace(filename);

    if (!trace.is_open()) {
        return {0xffffffff, 0xffffffff};
    }

    std::string address, _;
    CacheTestResult res;

    while (!trace.eof()) {
        getline(trace, _, ' ');
        getline(trace, address, ' ');
        getline(trace, _);

        if (address.length() == 0) {
            continue;
        }

        unsigned int addr = std::stol(address, nullptr, 16);

        res.hits += cache.check_cache(addr) ? 1 : 0;
        ++res.accesses;
    }

    return res;
}

int main() {
    unsigned int min_cache_size_log2 = 9, max_cache_size_log2 = 15;
    unsigned int min_line_size_log2 = 4, max_line_size_log2 = 9;

    std::string filenames[] = {"gcc.trace", "swim.trace"};
    std::ofstream results("../results.csv");

    if (!results.is_open()) {
        return 1;
    }

    const std::string header = "cache_size_log2,line_size_log2,set_size_log2,hits,accesses\n";
    results.write(header.c_str(), (long)header.length());

    for (unsigned int i = min_cache_size_log2; i <= max_cache_size_log2; ++i) {
        std::cout << 'i' << i << '\n';
        for (unsigned int j = min_line_size_log2; j <= max_line_size_log2; ++j) {
            for (unsigned int k = 0; k <= (i - j); ++k) {
                for (const auto& filename : filenames) {
                    auto res = test_cache(i, j, k, "../trace_files/" + filename);
                    if (res.accesses == 0xffffffff) {
                        std::cout << "Failed\n";
                        continue;
                    }
                    std::stringstream ss;
                    ss << i << ',' << j << ',' << k << ',' << res.hits << ',' << res.accesses << '\n';
                    const auto line = ss.str();
                    results.write(line.c_str(), (long)line.length());
                }
            }
        }
    }

    return 0;
}