#!/usr/bin/env python
import sys

import libs.colorizers
import libs.tokenizers

(candidate_language, precache) = libs.determine_language(sys.stdin)

candidate_language = candidate_language(colorscheme=libs.colorizers.Composite)

for line in precache + sys.stdin.readlines():
    tokens = candidate_language.tokenize(line[:-1])
    print(candidate_language.consume(tokens))
