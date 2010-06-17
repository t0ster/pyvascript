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

class Grammer(OMeta.makeGrammar(pyva_grammar, {}))):
    keywords = set(('break', 'case', 'catch', 'continue', 'default',
        'delete', 'do', 'else', 'finally', 'for', 'function', 'if', 'in',
        'instanceof', 'new', 'return', 'switch', 'this', 'throw', 'try',
        'typeof', 'var', 'void', 'while', 'with', ))
    hexDigits = '0123456789abcdef'

    def is_keyword(self, keyword):
         return keyword in self.keywords

translator_path = os.path.join(os.path.dirname(__file__), 'translator.ometa')
pyva_translator = open(translator_path, 'r').read()
Translator = OMeta.makeGrammar(pyva_translator, {'to_string': to_string})
