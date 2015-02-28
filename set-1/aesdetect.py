#!/usr/bin/python

import Crypto.Cipher.AES, os, sys, binascii

file_ = sys.argv[1:][0]

a = [binascii.unhexlify(s.strip()) for s in open(file_).readlines()]
c = []
for x in a:
    b = []
    for q in x:
        b.append(ord(q))
    c.append(b)

def get_blocks(stream, blocksize):
    for i in xrange(0, len(stream), blocksize):
        yield stream[i:i+blocksize]

def match_blocks(blocks, pivot):
    pivotblock, hits = blocks[pivot], 0
    for block in blocks:
        if pivotblock == block:
            hits += 1
    return hits

for line in c:
    blocks, hit = [block for block in get_blocks(line, 16)], False

    for n in xrange(10):
        if match_blocks(blocks, n) > 1:
            hit = True

    if hit:
        print binascii.hexlify(''.join([str(chr(p)) for p in line]))
