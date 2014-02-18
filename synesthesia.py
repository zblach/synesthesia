#!/usr/bin/env python
import sys

import libs.colorizers
import libs.tokenizers

#(candidate_language, precache) = libs.determine_language(sys.stdin)

#print >> sys.stderr, "using", candidate_language, "as language"
#print >> sys.stderr, "required", len(precache), "line(s) precached"

#candidate_language = candidate_language()
#candidate_language.set_color_scheme(libs.colorizers.Composite)

#for line in precache + sys.stdin.readlines():
    #tokens = candidate_language.tokenize(line[:-1])
    #print candidate_language.consume(tokens)
