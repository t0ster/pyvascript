from pyvascript.grammar import Grammar, Translator
import sys

g = Grammar.parse_source(open(sys.argv[1], 'r').read())
print g

print '\n------------------------------------------------------\n'

t = Translator.parse_source(g)
print t
