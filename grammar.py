import os.path
from pymeta.grammar import OMeta
import os

def to_string(string):
    string = repr(string)
    if string[0] == "'":
        string = '"' + string[1:-1].replace('"', r'\"') + '"'
    return string

grammar_path = os.path.join(os.path.dirname(__file__), 'grammar.ometa')
pyva_grammar = open(grammar_path, 'r').read()
Grammar = OMeta.makeGrammar(pyva_grammar, {})

translator_path = os.path.join(os.path.dirname(__file__), 'translator.ometa')
pyva_translator = open(translator_path, 'r').read()
Translator = OMeta.makeGrammar(pyva_translator, {'to_string': to_string})
