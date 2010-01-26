import os.path
from pymeta.grammar import OMeta
import os

grammar_path = os.path.join(os.path.dirname(__file__), 'grammar.ometa')
pyva_grammer = open(grammar_path, 'r').read()

Grammar = OMeta.makeGrammar(pyva_grammar, {}))