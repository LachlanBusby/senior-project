from tree import Tree
import nltk
import parser_utils
import re
from nltk.grammar import Nonterminal

class StmtParser(nltk.ViterbiParser):
	def __init__(self, grammar, trace=0):
		super(StmtParser, self).__init__(grammar, trace)

	def parse(self, tokens, stmt):
		""" generates parse tree for tokens, assumes literals have already been substituted """
		try:
			it = super(StmtParser, self).parse(tokens)
			for tree in it:
				t = parser_utils.convert_nltk_tree(tree)
				return self.post_process(t, stmt)
		except ValueError:
			missing = set()
			new_tokens = []
			for tok in tokens:
				if not self._grammar._lexical_index.get(tok):
					missing.add(tok)
					if not self.valid_var(tok): return self.error_node(stmt, missing)
					new_tokens.append(parser_utils.VAR_SUB)
				else:
					new_tokens.append(tok)

			try:
				it = super(StmtParser, self).parse(new_tokens)
				for nltk_t in it:
					t = parser_utils.convert_nltk_tree(nltk_t)
					t = self.post_process(t, stmt)
					t.children.append(self.warning_node(missing))
					return t
				return self.error_node(stmt, missing)
			except ValueError:
				return self.error_node(stmt, missing)

	def valid_var(self, tok):
		return re.match(r"^[A-Za-z]+[\w-]*\w$", tok) is not None

	def error_node(self, stmt, missing):
		if len(missing) == 1:
			error_str = stmt.strip() + "\t# ERROR. Unable to parse token: " + "".join(missing)
		else:
			error_str = stmt.strip() + "\t# ERROR. Unable to parse tokens: " + ", ".join(missing)
		return Tree("ERROR", children=[Tree("Error_Line", children=[Tree(error_str)])])

	def warning_node(self, missing):
		warning_str = "# WARNING. Interpreting as vars: " + ", ".join(missing)
		return Tree("Comment", children=[Tree(warning_str)])

	def post_process(self, tree, stmt):
		tokens = parser_utils.tokenize(stmt)
		tree.setWords(tokens)
		return tree