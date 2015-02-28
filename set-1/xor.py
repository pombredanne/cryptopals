#!/usr/bin/python

import os, sys, binascii, re

def ord_str(string):
        return [ord(c) for c in string]

def compute_hamming(st1, st2):
    if len(st1) != len(st2):
        raise ValueError
    l, hd = len(st1), 0
    for i in range(0, l):
	xred = st1[i] ^ st2[i]
	hd += len([c for c in bin(xred) if c == '1'])		
    return hd

def get_blocks(stream, blocksize):
        for i in xrange(0, len(stream), blocksize):
            yield stream[i:i+blocksize]

def attempt_key(stream, keylength):
        blockit = iter(get_blocks(stream, keylength))
        accum, size=0, len(stream)/keylength
        for i in range(size):
            try:
        	sl1, sl2 = next(blockit), next(blockit)
                accum += compute_hamming(sl1, sl2) / float(keylength)
            except StopIteration:
                pass
            except ValueError:
                size -= 1
	return  (keylength, accum / float(size))

def transpose(stream, keylength):
        pos, buckets = 0, [[] for _ in xrange(keylength)] 
        for b in stream:
            buckets[pos % keylength].append(b)
            pos += 1
        return buckets

def ascii_ratios(block):
    accum, total = {}, float(len(block))
    for c in block:
        for x in range(0, 255):
            xored = c^x
            if not x in accum:
                accum[x] = 0
            accum[x] += 1 if isAsciiChar(xored) else 0
    return accum

def isAsciiChar(c):
       return c in range(65, 90) or c in range(97, 122) or c == 32

kbeg = 2
kend = 40
scores = []

data = ord_str(binascii.a2b_base64("".join([s.strip() for s in open('6.txt').readlines()])))

for x in range(2, 40):
	scores.append(attempt_key(data, x))
scores.sort(key=lambda t: t[1])

bestres = scores[:1]
print 'using key length (%i) with lowest average Hamming distance (%f)' % bestres[0]

transposed = transpose(data, bestres[0][0])
keybytes = []

for num, block in enumerate(transposed):
    ratios = ascii_ratios(block)
    items = list(ratios.iteritems())
    items.sort(key=lambda k: k[1])
    items.reverse()

    keybytes.append(items[0][0])
    #print "%i:\t%s" % (num+1, " ".join([str(chr(x[0])) for x in items[:5]]))

print '#'*120
print 'KEY: ', ''.join([chr(b) for b in keybytes])
print '#'*120
plaintext = [chr(c ^ keybytes[n % len(keybytes)]) for n, c in enumerate(data)]
print ''.join(plaintext)
print '#'*120
