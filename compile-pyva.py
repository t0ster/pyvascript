#!/usr/bin/env python
from pyvascript.grammar import Grammar, Translator
import sys

if len(sys.argv) != 2:
    print >>sys.stderr, 'Usage: compile-pyva.py <script>'
    sys.exit(1)

file_name = sys.argv[1].rsplit('.', 1)[0]

fp = open(sys.argv[1], 'r')
source = fp.read()
fp.close()
g = Grammar.parse(source)

output = Translator.parse(g)
new_file = open(file_name + '.js', 'w')
new_file.write(output)
new_file.close()
