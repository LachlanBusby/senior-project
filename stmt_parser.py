import nltk
from nltk.grammar import Nonterminal

class StmtParser(nltk.ViterbiParser):

	def __init__(self, grammar, trace=0):
        super(PCFGStmtParser, self).__init__(grammar, trace)

    def parse(self, tokens):
    	""" 
    	generates parse tree for tokens,
    	assumes literals have already been substituted
    	"""

    	# TODO: add in support for unseen tokens???

    	return super(StmtParser, self).parse(tokens)
