//
// Created by anthony on 11/16/23.
//

#include "FIFOPolicy.h"

bool FIFOPolicy::access(std::unique_ptr<CacheLine[]> &cache, unsigned int offset, unsigned int tag,
                        unsigned int set_size_log2) {
    unsigned int set_size = 1 << set_size_log2;
    for (unsigned int i = 0u; i < set_size; ++i) {
        if (cache[offset+i].tag == tag) {
            return true;
        }

        if (cache[offset+i].tag == 0xFFFFFFFF) {
            cache[offset+i].tag = tag;
            cache[offset+i].priority = i + 1;
            return false;
        }
    }

    unsigned int argmin, min=set_size;
    for (unsigned int i = 0u; i < set_size; ++i) {
        if (cache[offset+i].priority < min) {
            min = cache[offset+i].priority;
            argmin = i;
        }
        --cache[offset+i].priority;
    }

    cache[offset+argmin].tag = tag;
    cache[offset+argmin].priority = set_size;

    return false;
}
