import os.path
from pymeta.grammar import OMeta
import os

grammar_path = os.path.join(os.path.dirname(__file__), 'grammar.ometa')
pyva_grammer = open(grammar_path, 'r').read()

class Grammer(OMeta.makeGrammar(pyva_grammar, {}))):
    def init(self):
        self.keywords = set(("break", "case", "catch", "continue", "default",
            "delete", "do", "else", "finally", "for", "function", "if", "in",
            "instanceof", "new", "return", "switch", "this", "throw", "try",
            "typeof", "var", "void", "while", "with", ))

    def is_keyword(self, keyword):
         return keyword in self.keywords

