from pseudo_parser import PseudoParser
from lollify import *
from python_codegen import *
import simple_examples

def test_args1():
	trees = [simple_examples.add_two_numbers()]
	stmts = simple_examples.add_two_numbers_stmts()
	return trees, stmts 

def test_args2():
	trees = [simple_examples.print_to_number()]
	stmts = simple_examples.print_to_number_stmts()
	return trees, stmts

def test_args3():
	trees = [simple_examples.add_two_numbers(), simple_examples.print_to_number()]
	stmts = simple_examples.add_two_numbers_stmts()
	return trees, stmts

def test_args4():
	trees = [simple_examples.add_two_numbers(), simple_examples.print_to_number()]
	stmts = simple_examples.print_to_number_stmts()
	return trees, stmts

def full_test(train_trees, test_trees):
	parse_tree = parser_test(test_trees)

def parser_test(train_trees, test_stmts):
	parser = PseudoParser.train(trees=train_trees)
	result = parser.parse(test_stmts)
	#print result.toString()
	return result

def lollify_test(tree):
	print tree.toString()
	
	ast = lollify_root(tree)
	print "\n\n\n"
	print ast
	
	code = emit_pycode(ast, None)
	print "\n\n\n"
	print code

# trees, stmts = test_args1()
# lollify_test(parser_test(trees, stmts))
#
# trees, stmts = test_args2()
# lollify_test(parser_test(trees, stmts))

trees, stmts = test_args3()
lollify_test(parser_test(trees, stmts))

# trees, stmts = test_args4()
# lollify_test(parser_test(trees, stmts))


parser = argparse.ArgumentParser(description='Run tests for Lollipop Pseudocode Compiler.')