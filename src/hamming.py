#!/usr/bin/python
#-*-coding:utf8-*-
'''
Author: zyy
Date: 2022-11-02 15:47:14
LastEditTime: 2022-11-02 17:02:21
Description: 
'''
import sys
# Compare calculates the Hamming distance between two 64-bit integers
# Currently, this is calculated using the Kernighan method [1]. Other methods
# exist which may be more efficient and are worth exploring at some point
# [1] http://graphics.stanford.edu/~seander/bithacks.html#CountBitsSetKernighan
def hamming_distance(hash_a, hash_b, hashsize = 64):
    x = (hash_a ^ hash_b) 
    distance = 0
    while x:
        distance += 1
        x &= x-1
    print(distance)
    return distance

def similarity(a, b):
    HashSize = 64
    return float(HashSize-hamming_distance(a, b)) / float(HashSize)

if __name__ == "__main__":
    hasha = int(sys.argv[1])
    hashb = int(sys.argv[2])
    dis = hamming_distance(hasha, hashb)
    print(dis)
    sim = similarity(hasha, hashb)
    print(sim)
   

