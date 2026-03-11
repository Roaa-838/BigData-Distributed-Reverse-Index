#!/usr/bin/env python3
import sys
import os
import string

filepath = os.environ.get('mapreduce_map_input_file', 'unknown_doc')
filename = os.path.basename(filepath)

stop_words = set()
try:
    with open('stopwords.txt', 'r') as f:
        for line in f:
            stop_words.add(line.strip().lower())
except IOError:
    pass

for line in sys.stdin:
    line = line.lower()
    translator = str.maketrans('', '', string.punctuation)
    line = line.translate(translator)
    words = line.strip().split()
    
    for word in words:
        if word and word not in stop_words:
            # We added a tab and a '1' here!
            print("{}\t{}\t1".format(word, filename))
