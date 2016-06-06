from tree import Tree
from test_utils import *
import parser_utils
import sys

def train_trees_all(do_not_include=[]):
	current_module = sys.modules[__name__]
	trees_names = [fn_name for fn_name in dir(current_module) if fn_name.endswith("_trees")]
	for tree in trees_names:
		for name in do_not_include:
			if tree.startswith(name):
				trees_names.remove(tree)

	print "All examples: %s" %trees_names
	return [current_module.__dict__[fn_name]() for fn_name in trees_names]

def add_two_numbers_trees():
	"""
	ADD-TWO-NUMBERS(a, b)
		c = a + b
		return c
	"""
	add_tree = add_expr("a", "b")
	assign_tree = assign_expr_tree("c", add_tree, indent=1, line=2)
	ret_tree = return_tree("c", indent=1, line=3)

	func_tree = func_def_tree("ADD-TWO-NUMBERS", ["a","b"])

	body_tree = func_tree.getStmtBody()
	body_tree.children.append(assign_tree)
	body_tree.children.append(Tree("STMT_LIST", indent=1, line=3, children=[ret_tree]))

	prog_body = Tree("STMT_LIST", indent=0, line=0, children=[func_tree])
	return Tree("PROGRAM", children=[prog_body])

def add_two_numbers_stmts():
	lines = []
	lines.append("ADD-TWO-NUMBERS(a, b)")
	lines.append("\tc = a + b")
	lines.append("\treturn c")
	return lines

# print add_two_numbers().toString()
# productions = {stmt_type: [] for stmt_type in parser_utils.STMT_TYPES}
# parser_utils.trees2productions([add_two_numbers()], productions)
# for p in productions:
# 	p_strs = []
# 	for r in productions[p]:
# 		p_strs.append(r.unicode_repr())
# 	print p + " : [" + "; ".join(p_strs) + "]"

def fibonacci_trees():
	"""
	FIBONACCI(N):
		if N == 1 or N == 2:
			return 1
		return FIBONACCI(N - 1) + FIBONACCI(N - 2)
	"""
	compop_tree1 = comp_op_val_int("N", "==", "1")
	compop_tree2 = comp_op_val_int("N", "==", "2")
	boolop_t = boolop_tree(compop_tree1, "or", compop_tree2)
	ret_tree1 = return_expr_tree(
		int_lit_tree("1"), indent=1, line=3)

	if_stmt_tree = if_expr_tree(boolop_t, indent=2, line=2)
	if_body = if_stmt_tree.getStmtBody()
	if_body.children.append(ret_tree1)

	binop_tree1 = bin_op_val_int("N", "-", "1")
	binop_tree2 = bin_op_val_int("N", "-", "2")
	call_tree1 = call_tree("FIBONACCI", [binop_tree1], parens=True, expr_args=True)
	call_tree2 = call_tree("FIBONACCI", [binop_tree2], parens=True, expr_args=True)

	binop_tree3 = binop_tree(call_tree1, "+", call_tree2)
	ret_tree2 = return_expr_tree(binop_tree3)
	func_tree = func_def_tree("FIBONACCI", ["N"])

	body_tree = func_tree.getStmtBody()
	body_tree.children.append(if_stmt_tree)
	body_tree.children.append(Tree("STMT_LIST", indent=1, line=3, children=[ret_tree2]))

	prog_body = Tree("STMT_LIST", indent=0, line=0, children=[func_tree])
	return Tree("PROGRAM", children=[prog_body])


def fibonacci_stmts():
	return ["FIBONACCI(N)", 
			"\tif N == 1 or N == 2",
			"\t\treturn 1",
			"\treturn FIBONACCI(N - 1) + FIBONACCI(N - 2)"]


def add_two_numbers_stmts():
	lines = []
	lines.append("ADD-TWO-NUMBERS(a, b)")
	lines.append("\tc = a + b")
	lines.append("\treturn c")
	return lines

def print_to_number_trees():
	"""
	PRINT-TO-NUMBER(N)
		for x = 0 to N
			print x
	"""
	start_expr = int_lit_tree("0")
	end_expr = var_tree("N")
	for_tree = for_range_tree("x", start_expr, end_expr, indent=1, line=2)

	call_t = call_tree("print", ["x"])
	print_tree = expr_stmt_tree(call_t, indent=2, line=3)

	for_body = for_tree.getStmtBody()
	for_body.children.append(print_tree)

	func_tree = func_def_tree("PRINT-TO-NUMBER", ["N"])
	body_tree = func_tree.getStmtBody()
	body_tree.children.append(for_tree)
	
	prog_body = Tree("STMT_LIST", indent=0, line=0, children=[func_tree])
	return Tree("PROGRAM", children=[prog_body])

def count_to_number_trees():
	"""
	COUNT-TO-TEN(start)
	    x = start
	    while x < 10
	        x += 1
        print x
	"""
	assign_tree = assign_expr_tree("x", var_tree("start"), indent=1, line=2)
	aug_assign_t = aug_assign_tree("x", "1", "+", indent=2, line=4)
	while_t = while_tree("x", "<", "10", indent=1, line=3)

	while_body = while_t.getStmtBody()
	while_body.children.append(aug_assign_t)

	call_t = call_tree("print", ["x"])
	print_tree = expr_stmt_tree(call_t, indent=2, line=3)

	while_stmt_tree = Tree("STMT_LIST", indent=0, line=0, children=[
		while_t,
		Tree("STMT_LIST", indent=1, line=5, children=[print_tree])])
		
	func_tree = func_def_tree("COUNT-TO-TEN", ["start"])
	body_tree = func_tree.getStmtBody()
	body_tree.children.append(assign_tree)
	body_tree.children.append(while_stmt_tree)

	prog_body = Tree("STMT_LIST", indent=0, line=0, children=[func_tree])
	return Tree("PROGRAM", children=[prog_body])

def count_to_number_stmts():
	lines = []
	lines.append("COUNT-TO-TEN(start)")
	lines.append("\tx = start")
	lines.append("\twhile x < 10")
	lines.append("\t\tx += 1")
	lines.append("\tprint x")
	return lines

def print_even_numbers_trees():
	"""
	PRINT-TO-NUMBER2(N)
		for x = 0 to N
			if x % 2 == 0
				print x

	PRINT-TO-NUMBER2(5)
	"""
	start_expr = int_lit_tree("0")
	end_expr = var_tree("N")
	for_tree = for_range_tree("x", start_expr, end_expr, indent=1, line=2)

	call_t = call_tree("print", ["x"])
	print_tree = expr_stmt_tree(call_t, indent=3, line=4)

	if_stmt_tree = if_binop_tree("x", "%", "2", "==", "0", indent=2, line=3)
	if_body = if_stmt_tree.getStmtBody()
	if_body.children.append(print_tree)

	for_body = for_tree.getStmtBody()
	for_body.children.append(if_stmt_tree)

	func_tree = func_def_tree("PRINT-TO-NUMBER2", ["N"])
	body_tree = func_tree.getStmtBody()
	body_tree.children.append(for_tree)

	call_tree2 = call_tree("PRINT-TO-NUMBER", ["5"], parens=True)
	exprstmt_tree = expr_stmt_tree(call_tree2, indent=0, line=5)
	
	prog_body = Tree("STMT_LIST", indent=0, line=0, children=[func_tree
		#, Tree("STMT_LIST", indent=0, line=5, children=[exprstmt_tree])
		])
	return Tree("PROGRAM", children=[prog_body])

# print print_to_number().toString()
def print_to_number_stmts():
	lines = []
	lines.append("PRINT-TO-NUMBER(N)")
	lines.append("\tfor x = 0 to N")
	lines.append("\t\tprint x")
	return lines

def print_even_numbers_stmts():
	lines = []
	lines.append("PRINT-TO-NUMBER2(N)")
	lines.append("\tfor x = 0 to N")
	lines.append("\t\tif x % 2 == 0")
	lines.append("\t\t\tprint x")
	#lines.append("PRINT-TO-NUMBER(5)")
	return lines


# is_even
def check_is_even_trees():
	"""
	IS-EVEN(N)
		return (N % 2) == 0

	IS-EVEN(4)
	"""
	bin_tree = bin_op_val_int('N', '%', '2')

	comp_tree = Tree("COMP_EXPR")
	comp_tree.children.append(Tree("EXPR",children=[bin_tree]))
	comp_tree.children.append(comp_operator_tree('=='))
	comp_tree.children.append(Tree("EXPR",children=[Tree("Int_Literal", children=[Tree('0')])]))
	
	ret_tree = Tree("RETURN")
	ret_tree.children.append(Tree("Return_Keyword",children=[Tree("return")]))
	ret_tree.children.append(comp_tree)
	
	return Tree("PROGRAM", children=[ret_tree])

def check_is_even_stmts():
	lines = []
	lines.append("IS-EVEN(N)")
	lines.append("\treturn (N % 2) == 0")
	return lines


def print_even_sum_trees():
	"""
	PRINT-EVEN-SUM(x, y)
		z = x + y
		if z % 2 == 0
			print z
	"""

	add_tree = add_expr("x", "y")
	assign_tree = assign_expr_tree("z", add_tree, indent=1, line=2)

	call_t = call_tree("print", ["z"])
	print_tree = expr_stmt_tree(call_t, indent=2, line=4)

	if_stmt_tree = if_binop_tree("z", "%", "2", "==", "0", indent=1, line=3)
	if_body = if_stmt_tree.getStmtBody()
	if_body.children.append(print_tree)

	func_tree = func_def_tree("PRINT-EVEN-SUM", ["x", "y"])

	body_tree = func_tree.getStmtBody()
	body_tree.children.append(assign_tree)
	body_tree.children.append(Tree("STMT_LIST", indent=1, line=3, children=[if_stmt_tree]))

	prog_body = Tree("STMT_LIST", indent=0, line=0, children=[func_tree])
	return Tree("PROGRAM", children=[prog_body])

def print_even_sum_stmts():
	lines = []
	lines.append("PRINT-EVEN-SUM(x, y)")
	lines.append("\tz = x + y")
	lines.append("\tif z % 2 == 0")
	lines.append("\t\tprint z")
	return lines


def if_less_trees():
	ret_n_tree = return_tree("n", indent=1, line=3)

	if_stmt_tree = if_tree("n", "<", "10", indent=1, line=2)
	if_body = if_stmt_tree.getStmtBody()
	if_body.children.append(ret_n_tree)

	else_ret_tree = return_val_tree("0", indent=1, line=3)

	func_tree = func_def_tree("IF-LESS-RETURN", ["n"])
	body_tree = func_tree.getStmtBody()
	body_tree.children.append(if_stmt_tree)
	body_tree.children.append(Tree("STMT_LIST", indent=1, line=3, children=[else_ret_tree]))

	prog_body = Tree("STMT_LIST", indent=0, line=0, children=[func_tree])
	return Tree("PROGRAM", children=[prog_body])

def if_less_stmts():
	lines = []
	lines.append("IF-LESS-RETURN(n)")
	lines.append("\tif n < 10")
	lines.append("\t\treturn n")
	lines.append("\treturn 0")
	return lines

def if_less_equal_trees():
	ret_n_tree = return_tree("n", indent=1, line=3)

	if_stmt_tree = if_tree("n", "<=", "10", indent=1, line=2)
	if_body = if_stmt_tree.getStmtBody()
	if_body.children.append(ret_n_tree)

	incr_tree = binop_tree(var_tree("n"), "+", int_lit_tree("1"))
	call_t = call_tree("IF-GREATER-EQUAL", [incr_tree], parens=True, expr_args=True)
	else_ret_tree = return_expr_tree(call_t, indent=1, line=4)

	func_tree = func_def_tree("IF-LEQ-RETURN", ["n"])
	body_tree = func_tree.getStmtBody()
	body_tree.children.append(if_stmt_tree)
	body_tree.children.append(Tree("STMT_LIST", indent=1, line=3, children=[else_ret_tree]))

	prog_body = Tree("STMT_LIST", indent=0, line=0, children=[func_tree])
	return Tree("PROGRAM", children=[prog_body])

def if_greater_trees():
	ret_n_tree = return_tree("n", indent=1, line=3)

	expr1 = var_tree("n")
	expr2 = binop_tree(var_tree("n"), "*", int_lit_tree("2"))
	cond_tree = compop_tree(expr1, ">", expr2)

	if_stmt_tree = if_expr_tree(cond_tree, indent=1, line=2)
	if_body = if_stmt_tree.getStmtBody()
	if_body.children.append(ret_n_tree)

	else_ret_tree = return_val_tree("0", indent=1, line=4)

	func_tree = func_def_tree("IF-GREATER-RETURN", ["n"])
	body_tree = func_tree.getStmtBody()
	body_tree.children.append(if_stmt_tree)
	body_tree.children.append(Tree("STMT_LIST", indent=1, children=[else_ret_tree]))

	prog_body = Tree("STMT_LIST", indent=0, line=0, children=[func_tree])
	return Tree("PROGRAM", children=[prog_body])

def if_greater_equal_trees():
	ret_n_tree = return_tree("n", indent=1, line=3)

	expr1 = var_tree("n")
	expr2 = int_lit_tree("10")
	cond1 = compop_tree(expr1, "<", expr2)

	expr3 = var_tree("n")
	expr4 = int_lit_tree("100")
	cond2 = compop_tree(expr3, ">=", expr4)

	or_tree = boolop_tree(cond1, "or", cond2)

	if_stmt_tree = if_expr_tree(or_tree, indent=1, line=2)
	if_body = if_stmt_tree.getStmtBody()
	if_body.children.append(ret_n_tree)

	else_ret_tree = return_val_tree("0", indent=1, line=4)

	func_tree = func_def_tree("IF-GEQ-RETURN", ["n"])
	body_tree = func_tree.getStmtBody()
	body_tree.children.append(if_stmt_tree)
	body_tree.children.append(Tree("STMT_LIST", indent=1, children=[else_ret_tree]))

	prog_body = Tree("STMT_LIST", indent=0, line=0, children=[func_tree])
	return Tree("PROGRAM", children=[prog_body])

def if_equal_trees():
	ret_n_tree = return_tree("n", indent=1, line=3)

	if_stmt_tree = if_tree("n", "==", "10", indent=1, line=2)
	if_body = if_stmt_tree.getStmtBody()
	if_body.children.append(ret_n_tree)

	else_ret_tree = return_val_tree("0", indent=1, line=4)

	func_tree = func_def_tree("IF-EQ-RETURN", ["n"])
	body_tree = func_tree.getStmtBody()
	body_tree.children.append(if_stmt_tree)
	body_tree.children.append(Tree("STMT_LIST", indent=1, children=[else_ret_tree]))

	prog_body = Tree("STMT_LIST", indent=0, line=0, children=[func_tree])
	return Tree("PROGRAM", children=[prog_body])

def bin_op_call_trees():
	call1 = call_tree("DO-SOMETHING", [var_tree("x")], parens=True, expr_args=True)
	call2 = call_tree("METHOD", [var_tree("x")], parens=True, expr_args=True)
	bin = binop_tree(call1, "%", call2)
	comp1 = compop_tree(bin, "<", var_tree("y"))

	expr1 = binop_tree(var_tree("y"), "-", int_lit_tree("2"))
	expr2 = binop_tree(int_lit_tree("100"), "/", var_tree("y"))
	comp2 = compop_tree(expr1, ">=", expr2)

	and_tree = boolop_tree(comp1, "and", comp2)
	if_stmt_tree = if_expr_tree(and_tree, indent=1, line=2)
	if_body = if_stmt_tree.getStmtBody()
	ret_true = return_expr_tree(bool_lit_tree("true"), indent=2, line=3)
	if_body.children.append(ret_true)

	else_ret_tree = return_expr_tree(bool_lit_tree("false"), indent=1, line=4)

	func_tree = func_def_tree("DUMB-METHOD", ["x", "y"])
	body_tree = func_tree.getStmtBody()
	body_tree.children.append(if_stmt_tree)
	body_tree.children.append(Tree("STMT_LIST", indent=1, line=4, children=[else_ret_tree]))

	prog_body = Tree("STMT_LIST", indent=0, line=0, children=[func_tree])
	return Tree("PROGRAM", children=[prog_body])

def bin_op_ret_trees():
	expr1 = binop_tree(var_tree("x"), "*", int_lit_tree("2"))
	expr2 = binop_tree(var_tree("x"), "-", int_lit_tree("10"))
	bin = binop_tree(expr1, "+", expr2)
	ret_tree = return_expr_tree(bin, indent=1, line=2)

	func_tree = func_def_tree("DUMB-METHOD2", ["x"])
	body_tree = func_tree.getStmtBody()
	body_tree.children.append(ret_tree)

	prog_body = Tree("STMT_LIST", indent=0, children=[func_tree])
	return Tree("PROGRAM", children=[prog_body])


def if_bin_comp(var, bin_op, comp_op, line_no, comp_val="true"):
	bin = binop_tree(var_tree(var), bin_op, int_lit_tree("2"))
	cond = compop_tree(bin, comp_op, bool_lit_tree(comp_val))
	if_stmt_tree = if_expr_tree(cond, indent=1, line=line_no)
	if_body = if_stmt_tree.getStmtBody()
	call = call_tree("print", [binop_tree(var_tree(var), bin_op, int_lit_tree("2"))], expr_args=True)
	if_body.children.append(call)

# def if_bin_trees():
# 	func_tree = func_def_tree("IF-BIN-METHOD", ["x"])
# 	body_tree = func_tree.getStmtBody()
# 	body_tree.children.append(if_bin_comp("x", "+", ">", 2))
#
# 	prog_body = Tree("STMT_LIST", indent=0, children=[func_tree])
# 	return Tree("PROGRAM", children=[prog_body])