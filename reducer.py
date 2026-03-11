#!/usr/bin/env python3
import sys

current_word = None
doc_counts = {}

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
        
    parts = line.split('\t')
    if len(parts) != 3:
        continue
        
    word, doc, count = parts[0], parts[1], int(parts[2])

    if current_word == word:
        doc_counts[doc] = doc_counts.get(doc, 0) + count
    else:
        if current_word is not None:
            docs_str = ", ".join(["{}:{}".format(d, c) for d, c in doc_counts.items()])
            print("{} --> {}".format(current_word, docs_str))
        current_word = word
        doc_counts = {doc: count}

if current_word is not None:
    docs_str = ", ".join(["{}:{}".format(d, c) for d, c in doc_counts.items()])
    print("{} --> {}".format(current_word, docs_str))
