from pseudo_parser import PseudoParser
import simple_examples

def simple_test():
	simple_trees = []
	simple_trees.append(simple_examples.add_two_numbers())

	parser = PseudoParser.train(trees=simple_trees)

# stmts = simple_examples.add_two_numbers_stmts()
# result = parser.parse(stmts)
# print result.toString()

simple_test()