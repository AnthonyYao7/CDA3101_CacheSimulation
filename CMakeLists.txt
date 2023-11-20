cmake_minimum_required(VERSION 3.25)
project(cache_sim)

set(CMAKE_CXX_STANDARD 14)

#if(NOT CMAKE_BUILD_TYPE)
#    set(CMAKE_BUILD_TYPE Release)
#endif()

set(CMAKE_CXX_FLAGS "-Wall -Wextra -g -Ofast")
set(CMAKE_CXX_FLAGS_DEBUG "-g")
#set(CMAKE_CXX_FLAGS_RELEASE "-O3")

add_executable(cache_sim
        Cache.h LRUPolicy.cpp FIFOPolicy.cpp main.cpp)
