from pseudo_parser import PseudoParser
from lollify import *
from python_codegen import *
import simple_examples
import argparse

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

def parser_test(train_trees, test_stmts, verbose=False):
	parser = PseudoParser.train(trees=train_trees)
	result = parser.parse(test_stmts)
	if verbose:
		print "\nParse Tree:"
		print result.toString()
	return result

def lollify_test(tree, verbose=False):
	ast = lollify_root(tree)
	if verbose:
		print "\nAST:"
		print ast
	return emit_pycode(ast, None)

def run_test(test_num, trees, stmts, parse_only, output):
	print "\n\nRunning test " + str(test_num) + "............................."
	if output >= 2:
		print "\nPseudocode:"
		for s in stmts: print s
	parse_tree = parser_test(trees, stmts, output==3)

	if not parse_only:
		code = lollify_test(parse_tree, output==3)
		if output >= 1:
			print "\nGenerated Code:"
			print code


# trees, stmts = test_args1()
# lollify_test(parser_test(trees, stmts))
#
# trees, stmts = test_args2()
# lollify_test(parser_test(trees, stmts))

# trees, stmts = test_args3()
# lollify_test(parser_test(trees, stmts))

# trees, stmts = test_args4()
# lollify_test(parser_test(trees, stmts))


parser = argparse.ArgumentParser(description='Run tests for Lollipop Pseudocode Compiler.')
parser.add_argument('test', nargs='?', type=int, choices=range(0,5), default=0, help="Specify the test number that you'd like to run, or 0 to run all.")
parser.add_argument('-p', '--parser', help='Run only the parser tests.', action='store_true')
parser.add_argument('-v', '--verbose', type=int, choices=range(0,4), default=2, help="Set the level of output. 0 - no output, 1 - source code only, 2 - pseudocode and source code, 3 - all intermediate output")

args = parser.parse_args()

if args.test == 0 or args.test == 1:
	trees, stmts = test_args1()
	run_test(1, trees, stmts, args.parser, args.verbose)

if args.test == 0 or args.test == 2:
	trees, stmts = test_args2()
	run_test(2, trees, stmts, args.parser, args.verbose)

if args.test == 0 or args.test == 3:
	trees, stmts = test_args3()
	run_test(3, trees, stmts, args.parser, args.verbose)

if args.test == 0 or args.test == 4:
	trees, stmts = test_args4()
	run_test(4, trees, stmts, args.parser, args.verbose)


