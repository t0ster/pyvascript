from pyvascript.grammar import Grammar, Translator
import  sys

file_name = sys.argv[1].rsplit('.', 1)[0]

g = Grammar.parse_source(open(sys.argv[1], 'r').read())

new_file = open(file_name + '.js', 'w')
new_file.write(Translator.parse_source(g))