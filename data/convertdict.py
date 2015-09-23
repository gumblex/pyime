#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys


def uniq(seq):  # Dave Kirby
    # Order preserving
    seen = set()
    return [x for x in seq if x not in seen and not seen.add(x)]


def pinyin(word):
    N = len(word)
    pos = 0
    result = []
    while pos < N:
        for i in range(N, pos, -1):
            frag = word[pos:i]
            if frag in chdict:
                result.append(sorted(chdict[frag], key=lambda x: -prob.get((frag, x), 0))[0])
                break
        pos = i
    return ' '.join(result)

chdict = {}
prob = {}
started = False

# Pass 1: Load Pinyin and its probability from dict
with open('luna_pinyin.dict.yaml', 'r', encoding='utf-8') as f:
    for ln in f:
        ln = ln.strip()
        if started and ln and ln[0] != '#':
            l = ln.split('\t')
            w, c = l[0], l[1]
            if w in chdict:
                chdict[w].append(c)
            else:
                chdict[w] = [c]
            if len(l) == 3:
                if l[2][-1] == '%':
                    p = float(l[2][:-1]) / 100
                else:
                    p = float(l[2])
                prob[(w, c)] = p
        elif ln == '...':
            started = True

essay = {}
# Pass 2: Load more words and word frequency
with open('essay.txt', 'r', encoding='utf-8') as f:
    for ln in f:
        word, freq = ln.strip().split('\t')
        # add-one smoothing
        essay[word] = int(freq) + 1
        if len(word) > 1:
            c = pinyin(word)
            if word not in chdict:
                chdict[word] = [c]

# Pass 3: Calculate (word, pinyin) pair frequency
final = []
for word, codes in chdict.items():
    for code in codes:
        freq = max(int(essay.get(word, 1) * prob.get((word, code), 1)), 1)
        final.append((word, code, freq))
final.sort()

with open('pinyin_rime.txt', 'w', encoding='utf-8') as f:
    for item in final:
        f.write('%s\t%s\t%s\n' % item)
