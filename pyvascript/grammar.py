from pymeta.grammar import OMeta
from pymeta.runtime import ParseError as OMetaParseError
import os

def compile(source):
    return Translator.parse_source(Grammar.parse_source(source))

grammar_path = os.path.join(os.path.dirname(__file__), 'grammar.ometa')
pyva_grammar = open(grammar_path, 'r').read()
def p(s):
    print s

class ParseError(Exception):
    pass

class BaseGrammar(object):
    @classmethod
    def parse_source(cls, source):
        try:
            return cls(source).apply('grammar')[0]
        except OMetaParseError, e:
            raise ParseError(e.formatError(source))

class Grammar(BaseGrammar, OMeta.makeGrammar(pyva_grammar, {'p': p})):
    keywords = set(('and', 'as', 'break', 'case', 'catch', 'class', 'continue',
        'def', 'default', 'del', 'delete', 'do', 'elif', 'else', 'except',
        'false', 'finally', 'for', 'function', 'if', 'in', 'is', 'instanceof',
        'new', 'not', 'null', 'or', 'pass', 'raise', 'return', 'switch',
        'this', 'throw', 'true', 'try', 'typeof', 'var', 'void', 'while',
        'with', 'yield',))
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
        'or': '||',
        'and': '&&',
        'is': '===',
        'is not': '!===',
    }
    name_map = {
        'None': 'null',
        'True': 'true',
        'False': 'false',
    }

    def __init__(self, *args, **kwargs):
        super(Translator, self).__init__(*args, **kwargs)
        self.indentation = 0
        self.local_vars = set()
        self.global_vars = set()
        self.var_stack = []
        self.temp_var_id = 0

    def make_temp_var(self, name, prefix='_$tmp'):
        self.temp_var_id += 1
        return '%s%s_%s' % (prefix, self.temp_var_id, name)

    def indent(self):
        self.indentation += 1
        return self.indentation

    def dedent(self):
        self.indentation -= 1

    def is_pure_var_name(self, var):
        return '.' not in var and '[' not in var

    def register_var(self, var):
        if self.is_pure_var_name(var) and var not in self.global_vars:
            self.local_vars.add(var)

    def register_vars(self, vars):
        for var in vars:
            self.register_var(var)

    def register_globals(self, vars):
        self.global_vars.update([var for var in vars if self.is_pure_var_name(var)])
        self.local_vars -= self.global_vars

    def push_vars(self):
        self.var_stack.append((self.local_vars, self.global_vars))
        self.local_vars = set()
        self.global_vars = set()

    def pop_vars(self):
        self.local_vars, self.global_vars = self.var_stack.pop()

    def make_block(self, stmts, indentation):
        indentstr = '  ' * indentation
        sep = '\n%s' % indentstr
        return '{\n%s%s\n%s}' % (indentstr, sep.join(stmts), '  ' * (indentation - 1))

    def make_func_block(self, stmts, indentation):
        indentstr = '  ' * indentation
        sep = '\n%s' % indentstr
        if self.local_vars:
            var = '%svar %s;\n%s' % (indentstr, ', '.join(sorted(self.local_vars)), indentstr)
        else:
            var = indentstr
        return '{\n%s%s\n%s}' % (var, sep.join(stmts), '  ' * (indentation - 1))

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

    def make_for(self, var, data, body):
        indentstr = '  ' * self.indentation
        datavar = self.make_temp_var('data')
        lenvar = self.make_temp_var('len')
        index = self.make_temp_var('index')
        init = 'var %s = _$pyva_iter(%s);\n%svar %s = %s.length;\n%s' % (
            datavar, data, indentstr, lenvar, datavar, indentstr)
        body = body.replace('{', '{\n%s%s = %s[%s];\n' % (indentstr + '  ', var, datavar, index), 1)
        return '%sfor (var %s = 0; %s < %s; %s++) %s' % (init, index, index, lenvar, index, body)

    def make_for_range(self, var, for_range, body):
        indentstr = '  ' * self.indentation
        step = '%s++' % var
        init = ''
        if len(for_range) == 1:
            start = 0
            end = self.make_temp_var('end')
            init = 'var %s = %s' % (end, for_range[0])
        elif len(for_range) == 2:
            start = self.make_temp_var('start')
            end = self.make_temp_var('end')
            init = 'var %s = %s, %s = %s' % (start, for_range[0], end, for_range[1])
        elif len(for_range) == 3:
            start = self.make_temp_var('start')
            end = self.make_temp_var('end')
            stepvar = self.make_temp_var('step')
            step = '%s += %s' % (var, stepvar)
            init = 'var %s = %s, %s = %s, %s = %s' % (start, for_range[0], end, for_range[1], stepvar, for_range[2])

        if init:
            init = '%s;\n%s' % (init, indentstr)
        return '%sfor (%s = %s; %s < %s; %s) %s' % (init, var, start, var, end,
                                                  step, body)

    def make_for_reversed_range(self, var, for_range, body):
        indentstr = '  ' * self.indentation
        step = '%s--' % var
        if len(for_range) == 1:
            return '%s = %s;\n%swhile (%s--) %s' % (var, for_range[0], indentstr, var, body)
        elif len(for_range) == 2:
            start = self.make_temp_var('start')
            end = self.make_temp_var('end')
            init = 'var %s = (%s) - 1, %s = %s' % (start, for_range[1], end, for_range[0])
        elif len(for_range) == 3:
            start = self.make_temp_var('start')
            end = self.make_temp_var('end')
            stepvar = self.make_temp_var('step')
            step = '%s -= %s' % (var, stepvar)
            init = 'var %s = (%s) - 1, %s = %s, %s = %s' % (start, for_range[1], end, for_range[0], stepvar, for_range[2])

        return '%s;\n%sfor (%s = %s; %s >= %s; %s) %s' % (init, indentstr, var,
                                                       start, var, end, step,
                                                       body)

    def make_func(self, name, args, body):
        if name:
            self.register_var(name[1])
            func = '%s = function' % name[1]
        else:
            func = 'function'
        return '%s(%s) %s' % (func, ', '.join(args), body)
