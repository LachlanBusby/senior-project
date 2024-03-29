from pseudo_parser import PseudoParser
from lollify import *
from python_codegen import *
from train_examples import *
import argparse

def test_args1():
	trees = [add_two_numbers_trees()]
	stmts = add_two_numbers_stmts()
	return trees, stmts 

def test_args2():
	trees = [print_to_number_trees()]
	stmts = print_to_number_stmts()
	return trees, stmts

def test_args3():
	trees = [add_two_numbers_trees(), print_to_number_trees()]
	stmts = add_two_numbers_stmts()
	return trees, stmts

def test_args4():
	trees = [add_two_numbers_trees(), print_to_number_trees()]
	stmts = print_to_number_stmts()
	return trees, stmts

def test_args5():
	trees = [add_two_numbers_trees(), print_to_number_trees(), print_even_numbers_trees()]
	stmts = print_to_number_stmts()
	return trees, stmts

def test_args6():
	trees = [print_even_sum_trees()]
	stmts = print_even_sum_stmts()
	return trees, stmts

def test_args7():
	trees = [add_two_numbers_trees(), print_to_number_trees(), print_even_numbers_trees()]
	stmts = print_even_sum_stmts()
	return trees, stmts

def test_args8():
	trees = [add_two_numbers_trees(), print_to_number_trees(), print_even_numbers_trees()]
	stmts = print_even_numbers_stmts()
	return trees, stmts

def test_args9():
	trees = [count_to_number_trees()]
	stmts = count_to_number_stmts()
	return trees, stmts

def test_args10():
	trees = [add_two_numbers_trees(), print_to_number_trees(), print_even_numbers_trees(), count_to_number_trees()]
	stmts = print_even_sum_stmts()
	return trees, stmts

def test_args11():
	trees = [if_less_trees(), if_less_equal_trees(), if_greater_trees(), if_greater_equal_trees(), if_equal_trees()]
	stmts = if_less_stmts()
	return trees, stmts

def test_args12():
	trees = [fibonacci_trees()]
	stmts = fibonacci_stmts()
	return trees, stmts

def test_args13():
	trees = train_trees_all(do_not_include=["fibonacci"])
	stmts = fibonacci_stmts()
	return trees, stmts

def test_args14():
	trees = train_trees_all()
	stmts = ["ERROR-TEST(x)", "\tif nonsense", "\t\treturn x", "\treturn 0"]
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
parser.add_argument('test', nargs='?', type=int, choices=range(0,15), default=0, help="Specify the test number that you'd like to run, or 0 to run all.")
parser.add_argument('-p', '--parser', help='Run only the parser tests.', action='store_true')
parser.add_argument('-v', '--verbose', type=int, choices=range(0,4), default=2, help="Set the level of output. 0 - no output, 1 - source code only, 2 - pseudocode and source code, 3 - all intermediate output")
parser.add_argument('-t', '--train-all', action='store_true', default=False, help="Train parser on all examples")
parser.add_argument('-e', '--examples', action='store_true', default=False, help="Print training examples.")

args = parser.parse_args()

#example_names = [fn_name.rpartition("_trees")[0] for fn_name in dir(train_examples) if fn_name.endswith("_trees")]
#sprint example_names
#examples = [(train_examples.__dict__[example_name + "_trees"], train_examples.__dict__[example_name + "_stmts"]) for example_name in example_names]

# def allTrees():
# 	return [trees() for trees, stmts in examples]

# if args.test == 0:
# 	for i, example in enumerate(examples):
# 		run_test(i, 
# 				[example[0]()] if not args.train_all else allTrees, 
# 				 example[1](), 
# 				 args.parser, args.verbose)
# else:
# 	run_test(args.test, 
# 				 [examples[args.test][0]()] if not args.train_all else allTrees, 
# 				 examples[args.test][1](), 
# 				 args.parser, args.verbose)	
# exit(0)

if args.examples:
	print "Training Examples"
	for t in train_trees_all(do_not_include=["fibonacci"]):
		print "\n"
		for s in t.getStmts():
			print s

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

if args.test == 0 or args.test == 13:
	trees, stmts = test_args13()
	run_test(13, trees, stmts, args.parser, args.verbose)

if args.test == 0 or args.test == 14:
	trees, stmts = test_args14()
	run_test(14, trees, stmts, args.parser, args.verbose)