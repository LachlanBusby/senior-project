from pseudo_parser import PseudoParser
import simple_examples
from lollify import lollify_root
from python_codegen import emit_pycode

def simple_test():
	simple_trees = []
	simple_trees.append(simple_examples.add_two_numbers())

	parser = PseudoParser.train(trees=simple_trees)
	stmts = simple_examples.add_two_numbers_stmts()
	result = parser.parse(stmts)
	print "#### Input 1 ####"
	print "\n".join(stmts).replace("\t", "    ")
	print "\n#### Result ####"
	ast = lollify_root(result)
	code = emit_pycode(ast, None)
	print code

def simple_test2():
	simple_trees = []
	simple_trees.append(simple_examples.print_to_number())

	parser = PseudoParser.train(trees=simple_trees)
	stmts = simple_examples.print_to_number_stmts()
	result = parser.parse(stmts)
	print "#### Input 2 ####"
	print "\n".join(stmts).replace("\t", "    ")
	print "\n#### Result ####"
	ast = lollify_root(result)
	code = emit_pycode(ast, None)
	print code

def simple_test3():
	simple_trees = []
	simple_trees.append(simple_examples.print_to_number2())
	# print simple_examples.print_to_number2()

	parser = PseudoParser.train(trees=simple_trees)
	stmts = simple_examples.print_to_number2_stmts()
	result = parser.parse(stmts)
	print "#### Input 3 ####"
	print "\n".join(stmts).replace("\t", "    ")
	print "\n#### Result ####"
	ast = lollify_root(result)
	code = emit_pycode(ast, None)
	print code


simple_test()
simple_test2()
simple_test3()