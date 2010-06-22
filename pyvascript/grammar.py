import os.path
from pymeta.grammar import OMeta
import os

grammar_path = os.path.join(os.path.dirname(__file__), 'grammar.ometa')
pyva_grammar = open(grammar_path, 'r').read()
def p(s):
    print s

class BaseGrammar(object):
    @classmethod
    def parse_source(cls, source):
        return cls(source).apply('grammar')[0]

class Grammar(BaseGrammar, OMeta.makeGrammar(pyva_grammar, {'p': p})):
    keywords = set(('as', 'break', 'case', 'catch', 'class', 'continue',
        'default', 'del', 'delete', 'do', 'elif', 'else', 'except', 'finally',
        'for', 'function', 'if', 'in', 'instanceof', 'new', 'pass', 'return',
        'self', 'switch', 'this', 'throw', 'try', 'typeof', 'var', 'void',
        'while', 'with', 'yield',))
    hex_digits = '0123456789abcdef'

    def __init__(self, *args, **kwargs):
        super(Grammar, self).__init__(*args, **kwargs)
        self.parenthesis = 0
        self.indent_stack = [0]

    def enter_paren(self):
        self.parenthesis += 1

    def leave_paren(self):
        self.parenthesis -= 1

    def dedent(self):
        # A dedent comes after a '\n'. Put it back, so the outer line
        # rule can handle the '\n'
        self.indent_stack.pop()
        input = self.input.prev()
        if input.head()[0] == '\n':
            self.input = input

    def is_keyword(self, keyword):
        return keyword in self.keywords

translator_path = os.path.join(os.path.dirname(__file__), 'translator.ometa')
pyva_translator = open(translator_path, 'r').read()
class Translator(BaseGrammar, OMeta.makeGrammar(pyva_translator, {})):
    op_map = {
        'not': '!',
        'del': 'delete ',
    }

    def to_string(self, string):
        string = repr(string)
        if string[0] == "'":
            string = '"' + string[1:-1].replace('"', r'\"') + '"'
        return string
