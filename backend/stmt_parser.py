from tree import Tree
import nltk
import parser_utils
from nltk.grammar import Nonterminal

class StmtParser(nltk.ViterbiParser):
	def __init__(self, grammar, trace=0):
		super(StmtParser, self).__init__(grammar, trace)

	
	def parse(self, tokens, stmt):
		""" generates parse tree for tokens, assumes literals have already been substituted """
		try:
			it = super(StmtParser, self).parse(tokens)
			for tree in it:
				return parser_utils.convert_nltk_tree(tree)
		except ValueError:
			error_str = stmt.strip() + "\t# ERROR: Unable to parse this line."
			return Tree("ERROR", children=[Tree("Error_Line", children=[Tree(error_str)])])

