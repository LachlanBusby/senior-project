from pseudo_parser import PseudoParser
from lollify import *
from python_codegen import *
from train_examples import *
import argparse

def test_args1():
	trees = [add_two_numbers()]
	stmts = add_two_numbers_stmts()
	return trees, stmts 

def test_args2():
	trees = [print_to_number()]
	stmts = print_to_number_stmts()
	return trees, stmts

def test_args3():
	trees = [add_two_numbers(), print_to_number()]
	stmts = add_two_numbers_stmts()
	return trees, stmts

def test_args4():
	trees = [add_two_numbers(), print_to_number()]
	stmts = print_to_number_stmts()
	return trees, stmts

def test_args5():
	trees = [add_two_numbers(), print_to_number(), print_to_number2()]
	stmts = print_to_number_stmts()
	return trees, stmts

def test_args6():
	trees = [print_even_sum()]
	stmts = print_even_sum_stmts()
	return trees, stmts

def test_args7():
	trees = [add_two_numbers(), print_to_number(), print_to_number2()]
	stmts = print_even_sum_stmts()
	return trees, stmts

def test_args8():
	trees = [add_two_numbers(), print_to_number(), print_to_number2()]
	stmts = print_to_number2_stmts()
	return trees, stmts

def test_args9():
	trees = [count_to_number()]
	stmts = count_to_number_stmts()
	return trees, stmts

def test_args10():
	trees = [add_two_numbers(), print_to_number(), print_to_number2(), count_to_number()]
	stmts = print_even_sum_stmts()
	return trees, stmts

def test_args11():
	trees = [if_less(), if_less_equal(), if_greater(), if_greater_equal(), if_equal()]
	stmts = if_less_stmts()
	return trees, stmts

def test_args12():
	trees = [fibonacci()]
	stmts = fibonacci_stmts()
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
	if output >= 1:
		print "\nPseudocode:"
		print "\n".join(stmts).replace("\t", "    ")
	parse_tree = parser_test(trees, stmts, output==3)

	if not parse_only:
		code = lollify_test(parse_tree, output==3)
		if output >= 1:
			print "\nGenerated Code:"
			print code


parser = argparse.ArgumentParser(description='Run tests for Lollipop Pseudocode Compiler.')
parser.add_argument('test', nargs='?', type=int, choices=range(0,13), default=0, help="Specify the test number that you'd like to run, or 0 to run all.")
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

if args.test == 0 or args.test == 5:
	trees, stmts = test_args5()
	run_test(5, trees, stmts, args.parser, args.verbose)

if args.test == 0 or args.test == 6:
	trees, stmts = test_args6()
	run_test(6, trees, stmts, args.parser, args.verbose)

if args.test == 0 or args.test == 7:
	trees, stmts = test_args7()
	run_test(7, trees, stmts, args.parser, args.verbose)

if args.test == 0 or args.test == 8:
	trees, stmts = test_args8()
	run_test(8, trees, stmts, args.parser, args.verbose)

if args.test == 0 or args.test == 9:
	trees, stmts = test_args9()
	run_test(9, trees, stmts, args.parser, args.verbose)

if args.test == 0 or args.test == 10:
	trees, stmts = test_args10()
	run_test(10, trees, stmts, args.parser, args.verbose)

if args.test == 0 or args.test == 11:
	trees, stmts = test_args11()
	run_test(11, trees, stmts, args.parser, args.verbose)

if args.test == 0 or args.test == 12:
	trees, stmts = test_args12()
	run_test(12, trees, stmts, args.parser, args.verbose)