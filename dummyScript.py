#!/usr/bin/env python3
# This script may or may not be helpful during debugging
# Written by Jude Hungerford
import sys
GOLEM_WORKDIR = '/golem/work/'
args = sys.argv[1:]
print(args)
with open(F'{GOLEM_WORKDIR}err2.log', 'w') as f:
    f.write(str(args))
    f.write('\nabcde')

