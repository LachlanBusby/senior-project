from pseudo_parser import PseudoParser
from lollify import *
from python_codegen import *
import simple_examples

def simple_test1():
	simple_trees = []
	simple_trees.append(simple_examples.add_two_numbers())

	parser = PseudoParser.train(trees=simple_trees)
	stmts = simple_examples.add_two_numbers_stmts()
	result = parser.parse(stmts)
	return result
	print result.toString()

def simple_test2():
	simple_trees = []
	simple_trees.append(simple_examples.print_to_number())

	parser = PseudoParser.train(trees=simple_trees)
	stmts = simple_examples.print_to_number_stmts()
	result = parser.parse(stmts)
	return result
	print result.toString()

def lollify_test1():
	tree = simple_test1()
	print tree.toString()
	ast = lollify_root(tree)
	print ast
	emit_pycode(ast, None)

def lollify_test2():
	tree = simple_test2()
	print tree.toString()
	ast = lollify_root(tree)
	print ast
	emit_pycode(ast, None)

lollify_test2()
#simple_test1()