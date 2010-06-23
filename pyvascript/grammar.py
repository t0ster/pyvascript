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
    keywords = set(('as', 'break', 'case', 'catch', 'class', 'continue', 'def',
        'default', 'del', 'delete', 'do', 'elif', 'else', 'except', 'finally',
        'for', 'function', 'if', 'in', 'instanceof', 'new', 'pass', 'raise',
        'return', 'switch', 'this', 'throw', 'try', 'typeof', 'var', 'void',
        'while', 'with', 'yield',))
    hex_digits = '0123456789abcdef'

    def __init__(self, *args, **kwargs):
        super(Grammar, self).__init__(*args, **kwargs)
        self.parenthesis = 0
        self.parenthesis_stack = []
        self.indent_stack = [0]

    def enter_paren(self):
        self.parenthesis += 1

    def leave_paren(self):
        self.parenthesis -= 1

    def enter_deflambda(self, indent):
        self.indent_stack.append(indent)
        self.parenthesis_stack.append(self.parenthesis)
        self.parenthesis = 0

    def leave_deflambda(self):
        self.indent_stack.pop()
        self.parenthesis = self.parenthesis_stack.pop()

    def get_indent(self):
        for index in reversed(range(self.input.position)):
            if self.input.data[index] == '\n':
                return self.input.position - (index + 1)
        return 0

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
class Translator(BaseGrammar, OMeta.makeGrammar(pyva_translator, {'p': p})):
    op_map = {
        'not': '!',
        'del': 'delete ',
    }
    
    binop_map = {
    }

    def __init__(self, *args, **kwargs):
        super(Translator, self).__init__(*args, **kwargs)
        self.indentation = 0

    def indent(self):
        self.indentation += 1
        return self.indentation

    def dedent(self):
        self.indentation -= 1

    def make_block(self, stmts, indentation):
        indentstr = '  ' * indentation
        sep = '\n%s' % indentstr
        return '{\n%s%s\n%s}' % (indentstr, sep.join(stmts), '  ' * (indentation - 1))

    def make_dict(self, items, indentation):
        indentstr = '  ' * indentation
        sep = ',\n%s' % indentstr
        return '{\n%s%s\n%s}' % (indentstr, sep.join(items), '  ' * (indentation - 1))

    def make_if(self, cond, block, elifexprs, elseblock):
        expr = ['if (%s) %s' % (cond, block)]
        expr.extend('else if (%s) %s' % x for x in elifexprs)
        if elseblock:
            expr.append('else %s' % elseblock)
        return ' '.join(expr)

    def make_func(self, name, args, body):
        if name:
            func = '%s = function' % name[1]
        else:
            func = 'function'
        return '%s(%s) %s' % (func, ', '.join(args), body)

    def to_string(self, string):
        string = repr(string)
        if string[0] == "'":
            string = '"' + string[1:-1].replace('"', r'\"') + '"'
        return string
