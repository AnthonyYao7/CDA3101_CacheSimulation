//
// Created by anthony on 11/16/23.
//

#ifndef CACHE_SIM_CACHE_H
#define CACHE_SIM_CACHE_H

#include <memory>
#include <bitset>
#include <iostream>
#include <cstring>

struct CacheLine {
    unsigned int tag;
    unsigned int priority;
};

/**
 *
 * @tparam P Replacement Policy
 */
template <class P>
class Cache {
private:


    unsigned int _cache_size_log2, _line_size_log2, _set_size_log2;
    unsigned int _num_lines_log2, _num_sets_log2;
    unsigned int _set_mask{}, _tag_mask{};

    std::unique_ptr<CacheLine[]> _cache;
public:

    /**
     *
     * @param cache_size_log2 log base 2 of the number of bytes in the cache
     * @param line_size_log2 log base 2 of the number of bytes in a line
     * @param set_size_log2 log base 2 of the number of lines in a set
     */
    Cache(unsigned int cache_size_log2, unsigned int line_size_log2, unsigned int set_size_log2)  :
            _cache_size_log2(cache_size_log2),
            _line_size_log2(line_size_log2),
            _set_size_log2(set_size_log2),
            _num_lines_log2(cache_size_log2 - line_size_log2),
            _num_sets_log2(_num_lines_log2 - set_size_log2),
            _cache(new CacheLine[1<<cache_size_log2]) {

        for (unsigned int i = 0, m=1; i < 32; ++i, m<<=1) {
            if (i >= _line_size_log2 and i < _line_size_log2 + _num_sets_log2) {
                _set_mask = _set_mask | m;
            }
            if (i >= _line_size_log2 + _num_sets_log2) {
                _tag_mask = _tag_mask | m;
            }
        }

        memset(_cache.get(), 0xFF, (1<<cache_size_log2) * sizeof(CacheLine));

        std::bitset<32> _line_mask_print(_set_mask), _tag_mask_print(_tag_mask);
        std::cout << _line_mask_print << '\n' << _tag_mask_print << '\n';
    }

    bool check_cache(unsigned int address) {
        unsigned int tag = address & _tag_mask;
        unsigned int set = address & _set_mask;

        /* num_sets * lines / set * bytes / line = byte offset */
        auto set_start = set * (1 << _set_size_log2);

        return P::access(_cache, set_start, tag, _set_size_log2);
    }
};


#endif //CACHE_SIM_CACHE_H
