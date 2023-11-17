//
// Created by anthony on 11/16/23.
//

#ifndef CACHE_SIM_FIFOPOLICY_H
#define CACHE_SIM_FIFOPOLICY_H

#include <memory>
#include "Cache.h"


class FIFOPolicy {
public:
    static bool
    access(std::unique_ptr<CacheLine[]> &cache, unsigned int offset, unsigned int tag, unsigned int set_size_log2);
};


#endif //CACHE_SIM_FIFOPOLICY_H
