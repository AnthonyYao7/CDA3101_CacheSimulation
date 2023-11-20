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

template <class P>
CacheTestResult test_cache(unsigned int cache_size_log2, unsigned int line_size_log2, unsigned int set_size_log2, const std::string& filename) {
    Cache<P> cache(cache_size_log2, line_size_log2, set_size_log2);

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
    unsigned int min_cache_size_log2 = 9, max_cache_size_log2 = 14;
    unsigned int min_line_size_log2 = 3, max_line_size_log2 = 8;

    std::string filenames[] = {"gcc.trace"};
    std::ofstream lru_results("../LRUresults.csv");
    if (!lru_results.is_open()) {
        return 1;
    }
    std::ofstream fifo_results("../FIFOresults.csv");
    if (!fifo_results.is_open()) {
        return 1;
    }

    const std::string header = "cache_size_log2,line_size_log2,set_size_log2,hits,accesses\n";
    lru_results.write(header.c_str(), (long)header.length());
    fifo_results.write(header.c_str(), (long)header.length());

    for (unsigned int i = min_cache_size_log2; i <= max_cache_size_log2; ++i) {
        std::cout << 'i' << i << '\n';
        for (unsigned int j = min_line_size_log2; j <= max_line_size_log2; ++j) {
            for (unsigned int k = 0; k <= (i - j); ++k) {
                for (const auto& filename : filenames) {
                    auto lru_res = test_cache<LRUPolicy>(i, j, k, "../trace_files/" + filename);
                    if (lru_res.accesses == 0xffffffff) {
                        std::cout << "Failed\n";
                        continue;
                    }
                    std::stringstream lru_ss;
                    lru_ss << i << ',' << j << ',' << k << ',' << lru_res.hits << ',' << lru_res.accesses << '\n';
                    const auto lru_line = lru_ss.str();
                    lru_results.write(lru_line.c_str(), (long)lru_line.length());

                    auto fifo_res = test_cache<FIFOPolicy>(i, j, k, "../trace_files/" + filename);
                    if (fifo_res.accesses == 0xffffffff) {
                        std::cout << "Failed\n";
                        continue;
                    }
                    std::stringstream fifo_ss;
                    fifo_ss << i << ',' << j << ',' << k << ',' << fifo_res.hits << ',' << fifo_res.accesses << '\n';
                    const auto fifo_line = fifo_ss.str();
                    fifo_results.write(fifo_line.c_str(), (long)fifo_line.length());
                }
            }
        }
    }

    return 0;
}