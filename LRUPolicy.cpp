//
// Created by anthony on 11/16/23.
//

#include "LRUPolicy.h"

bool LRUPolicy::access(std::unique_ptr<CacheLine[]> &cache, unsigned int offset, unsigned int tag,
                       unsigned int set_size_log2) {
    unsigned int set_size = 1 << set_size_log2, ind;
    bool hit = false;
    CacheLine* c = cache.get();
    for (unsigned int i = 0u; i < set_size; ++i) {
        if (c[offset+i].tag == tag) {
            hit = true;
            ind = i;
            break;
        }

        if (c[offset+i].tag == 0xFFFFFFFF) {
            c[offset+i].tag = tag;
            c[offset+i].priority = i;
            return false;
        }
    }

    if (hit) {
        unsigned int i;
        for (i = 0; i < set_size; ++i) {
            if (c[offset+i].tag == 0xFFFFFFFF) {
                break;
            }
            if (c[offset+i].priority > c[offset+ind].priority) {
                --c[offset+i].priority;
            }
        }
        c[offset+ind].priority = i-1;
    } else {
        unsigned int argmin;
        for (unsigned int i = 0; i < set_size; ++i) {
            if (c[offset+i].priority == 0) {
                argmin = i;
            }
            --c[offset+i].priority;
        }
        c[offset+argmin].priority = set_size-1;
        c[offset+argmin].tag = tag;
    }

    return hit;
}
