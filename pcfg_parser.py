import tree;
import constituent;
import Grammar;


class PCFGParser:
	
	VERBOSE = True

	Lexicon lexicon
	Grammar grammar

	def train(self, train_trees):
		if (VERBOSE) print("\nTraining..............................................\n")

		train_trees[:] = [TreeAnnotations.annotateTree(tree) for tree in train_trees]

		lexicon = Lexicon(train_trees)
		grammar = Grammar(train_trees)

		if (VERBOSE):
			print("\tLexicon:\n" + lexicon.wordToTagCounters.toString())
			print("\n\n\tGrammar:\n" + grammar.toString())

		train_trees[:] = [TreeAnnotations.annotateTree(tree) for tree in train_trees]


	def getBestParse(statements):
		if (VERBOSE):
			full_program = "\n".join(statements)
			print("\nGetting best parse for \"" + full_program + "\'...........................................")

		numStatements = statements.len()

		programTree = tree("ROOT", -1)
		parentNode = programTree
		for (stmt : statements):
			indent = len(stmt) - len(stmt.lstrip('\t'))
			while (indent <= parentNode.getIndent()):
				parentNode = parentNode.getParent()
			parentNode = parseStatement(stmt, parentNode)


	def parseStatement(stmt, parentNode):
		# TODO: this should use Viterbi scores (see 224n PCFG parser)

