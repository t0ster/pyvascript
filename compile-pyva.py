#!/usr/bin/env python
from pyvascript.grammar import Grammar, Translator
import sys

if len(sys.argv) != 2:
    print >>sys.stderr, 'Usage: compile-pyva.py <script>'
    sys.exit(1)

file_name = sys.argv[1].rsplit('.', 1)[0]

g = Grammar.parse_source(open(sys.argv[1], 'r').read())

new_file = open(file_name + '.js', 'w')
new_file.write(Translator.parse_source(g))
