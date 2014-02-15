#!/usr/bin/env python
import libs.colorizers
import libs.tokenizers

tokenator = libs.tokenizers.XXDTokenizer()
tokenator.setcolor(libs.colorizers.Composite)

import sys

for line in sys.stdin.readlines():
    tokens = tokenator.tokenize(line[:-1])
    print tokenator.consume(tokens)
