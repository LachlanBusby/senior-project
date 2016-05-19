import Tree
import StmtClassifier
import StmtParser
from nltk.tokenize import wordpunct_tokenize
from nltk.grammar import WeightedProduction, Nonterminal
from parser_utils import substitute_literals, restore_literals, corpus2trees, trees2productions, trees2stmts, 

class PseudoParser():
	
	STMT_TYPES = ["FUNC_DEF", "RETURN", "ASSIGN", "AUG_ASSIGN", "FOR_RANGE", "FOR_EACH", "WHILE", "IF", "BREAK", "CONTINUE", "EXPR_STMT"]
	ROOT_TYPE = "PROGRAM"

	def __init__(self, productions, stmts, stmt_types):
		self.parsers = {}
		for stmt_type in productions:
			pcfg = nltk.grammar.induce_pcfg(nltk.grammar.Nonterminal(stmt_type), productions)
			self.parsers[stmt_type] = StmtParser(pcfg)	
		
		self.clf = StmtClassifier()
		self.clf.train(stmts,stmt_types)


	@staticmethod
	def _preprocess(trees):
		subs = []
		for t in trees:
			orig_yield = t.getYield()
			sub_yield, t_subs = substitute_literals(orig_yield)
			t.setWords(sub_yield)
			subs.append(t_subs)
		return trees, subs

	@staticmethod
	def _postprocess(trees, substitutions):
		for idx, t in enumerate(trees):
			sub_yield = t.getYield()
			orig_yield = restore_literals(sub_yield, substitutions[idx])
			t.setWords(orig_yield)
		return trees

	@classmethod
	def train(cls,filename):
		with open(filename, 'r') as f:
			corpus = f.read()
		trees = parser_utils.corpus2trees(corpus)
		trees, subs = self._preprocess(trees)

		productions = {stmt_type: [] for stmt_type in STMT_TYPES}
		trees2productions(trees, productions)

		stmts, types = trees2stmts(trees)

		return cls(productions, stmts, types)

	@staticmethod
	def _tokenize(stmt):
		tokens = wordpunct_tokenize(stmt)
		tokens, subs = substitute_literals(tokens)
		return tokens

	@staticmethod
	def _setStmtYield(tree,stmt):
		tokens = wordpunct_tokenize(stmt)
		tree.setWords(tokens)
		return tree

	def parse(self, stmts):
		""" takes in a list of lines/statements and returns full parse tree """
		numStatements = stmts.len()
		tree = Tree("PROGRAM")
		parentNode = tree
		for line,stmt : enumerate(statements):
			indent = len(stmt) - len(stmt.lstrip('\t'))
			while not (parentNode.isStmtList() or parentNode.isStmt()) or indent <= parentNode.getIndent():
				parentNode = parentNode.getParent()
			
			if parentNode.isStmt():	
				parentNode = parentNode.children[0]
				list_tree = Tree("STMT_LIST", indent)
				parentNode.children.append(list_tree)
				parentNode = list_tree
			
			if len(parentNode.children) == 1:
				list_tree = Tree("STMT_LIST", indent)
				parentNode.children.append(list_tree)
				parentNode = list_tree
			
			tokens = self._tokenize(stmt)
			stmt_type = self.clf.classify_stmt(" ".join(tokens))
			stmt_tree = Tree("STMT", indent, line)
			stmt_tree.children.append(self.parsers[stmt_type].parse(tokens))
			stmt_tree = self._setStmtYield(stmt_tree,stmt)
			parentNode.children.append(stmt_tree)
			parentNode = stmt_tree
		return tree


			


