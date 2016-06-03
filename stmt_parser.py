import nltk
import parser_utils
from nltk.grammar import Nonterminal

class StmtParser(nltk.ViterbiParser):
	def __init__(self, grammar, trace=0):
		super(StmtParser, self).__init__(grammar, trace)

	
	def parse(self, tokens):
		""" generates parse tree for tokens, assumes literals have already been substituted """
    	# TODO: add in support for unseen tokens???
		it = super(StmtParser, self).parse(tokens)
		for tree in it:
			return parser_utils.convert_nltk_tree(tree)
		return None
