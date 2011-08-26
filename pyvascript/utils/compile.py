from pyvascript.grammar import Grammar, Translator


def compile_pyva(source):
    grammar = Grammar.parse(source)
    return Translator.parse(grammar)
