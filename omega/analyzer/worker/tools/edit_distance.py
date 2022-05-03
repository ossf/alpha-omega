# Copyright (C) Microsoft Corporation, All rights reserved.

from Levenshtein import distance
import sys
import re


if len(sys.argv) != 3:
    print("Usage: edit_distance.py word \"list|of|words\"")
    sys.exit(1)

target = sys.argv[1].lower().replace("@", "-").replace("/", "-")
targets = list(filter(lambda t: t, re.split('[_-]', target)))
needles = sys.argv[2].lower().split('|')

for target in targets:
    for needle in needles:
        d = distance(target, needle)
        if d == 0:
            print(f"EXACT MATCH: {target}")
        else:
            dist_pct = float(d) / float(len(target))
            if (len(target) <= 5 and dist_pct < 0.25) or dist_pct < 0.185:
                print(f"SIMILAR MATCH: {target} <=> {needle}")
