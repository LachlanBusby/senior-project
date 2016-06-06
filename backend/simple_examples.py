from tree import Tree
import test_utils
import parser_utils

def add_two_numbers():
	"""
	ADD-TWO-NUMBERS(a,b)
		c = a + b
		return c
	"""
	add_tree = test_utils.add_expr("a", "b")
	assign_tree = test_utils.assign_expr_tree("c", add_tree, indent=1, line=2)
	ret_tree = test_utils.return_tree("c", indent=1, line=3)

	func_tree = test_utils.func_def_tree("ADD-TWO-NUMBERS", ["a","b"])

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

def fibonacci():
	"""
	FIBONACCI(N):
		if N == 1 or N == 2:
			return 1
		return FIBONACCI(N - 1) + FIBONACCI(N - 2)
	"""
	compop_tree1 = test_utils.comp_op_val_int("N", "==", "1")
	compop_tree2 = test_utils.comp_op_val_int("N", "==", "2")
	boolop_tree = test_utils.boolop_tree(compop_tree1, "or", compop_tree2)
	ret_tree1 = test_utils.return_expr_tree(
		test_utils.int_lit_tree("1"), indent=1, line=3)

	if_tree = test_utils.if_expr_tree(boolop_tree, indent=2, line=2)
	if_body = if_tree.getStmtBody()
	if_body.children.append(ret_tree1)

	binop_tree1 = test_utils.bin_op_val_int("N", "-", "1")
	binop_tree2 = test_utils.bin_op_val_int("N", "-", "2")
	call_tree1 = test_utils.call_tree("FIBONACCI", [binop_tree1], parens=True, expr_args=True)
	call_tree2 = test_utils.call_tree("FIBONACCI", [binop_tree2], parens=True, expr_args=True)

	binop_tree3 = test_utils.binop_tree(call_tree1, "+", call_tree2)
	ret_tree2 = test_utils.return_expr_tree(binop_tree3)
	func_tree = test_utils.func_def_tree("FIBONACCI", ["N"])

	body_tree = func_tree.getStmtBody()
	body_tree.children.append(if_tree)
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

def print_to_number():
	"""
	PRINT-TO-NUMBER(N)
		for x = 0 to N + 1
			print x
	"""
	start_expr = test_utils.int_lit_tree("0")
	end_expr = test_utils.var_tree("N")
	for_tree = test_utils.for_range_tree("x", start_expr, end_expr, indent=1, line=2)

	call_tree = test_utils.call_tree("print", ["x"])
	print_tree = test_utils.expr_stmt_tree(call_tree, indent=2, line=3)

	for_body = for_tree.getStmtBody()
	for_body.children.append(print_tree)

	func_tree = test_utils.func_def_tree("PRINT-TO-NUMBER", ["N"])
	body_tree = func_tree.getStmtBody()
	body_tree.children.append(for_tree)
	
	prog_body = Tree("STMT_LIST", indent=0, line=0, children=[func_tree])
	return Tree("PROGRAM", children=[prog_body])

def count_to_number():
	"""
	COUNT-TO-TEN(START)
	    x = start
	    while x < 10
	        x += 1
        print x
	"""
	assign_tree = test_utils.assign_expr_tree("x", test_utils.var_tree("START"), indent=1, line=2)
	aug_assign_tree = test_utils.aug_assign_tree("x", "1", "+", indent=2, line=4)
	while_tree = test_utils.while_tree("x", "<", "10", indent=1, line=3)

	while_body = while_tree.getStmtBody()
	while_body.children.append(aug_assign_tree)

	call_tree = test_utils.call_tree("print", ["x"])
	print_tree = test_utils.expr_stmt_tree(call_tree, indent=2, line=3)

	while_stmt_tree = test_utils.Tree("STMT_LIST", indent=0, line=0, children=[
		while_tree, 
		Tree("STMT_LIST", indent=1, line=5, children=[print_tree])])
		
	func_tree = test_utils.func_def_tree("COUNT-TO-TEN", ["START"])
	body_tree = func_tree.getStmtBody()
	body_tree.children.append(assign_tree)
	body_tree.children.append(while_stmt_tree)

	prog_body = Tree("STMT_LIST", indent=0, line=0, children=[func_tree])
	return Tree("PROGRAM", children=[prog_body])

def count_to_number_stmts():
	lines = []
	lines.append("COUNT-TO-TEN(START)")
	lines.append("\tx = START")
	lines.append("\twhile x < 10")
	lines.append("\t\tx += 1")
	lines.append("\tprint x")
	return lines

def print_to_number2():
	"""
	PRINT-TO-NUMBER2(N)
		for x = 0 to N + 1
			if x % 2 == 0
				print x

	PRINT-TO-NUMBER2(5)
	"""
	start_expr = test_utils.int_lit_tree("0")
	end_expr = test_utils.var_tree("N")
	for_tree = test_utils.for_range_tree("x", start_expr, end_expr, indent=1, line=2)

	call_tree = test_utils.call_tree("print", ["x"])
	print_tree = test_utils.expr_stmt_tree(call_tree, indent=3, line=4)

	if_tree = test_utils.if_binop_tree("x", "%", "2", "==", "0", indent=2, line=3)
	if_body = if_tree.getStmtBody()
	if_body.children.append(print_tree)

	for_body = for_tree.getStmtBody()
	for_body.children.append(if_tree)

	func_tree = test_utils.func_def_tree("PRINT-TO-NUMBER2", ["N"])
	body_tree = func_tree.getStmtBody()
	body_tree.children.append(for_tree)

	call_tree2 = test_utils.call_tree("PRINT-TO-NUMBER", ["5"], parens=True)
	exprstmt_tree = test_utils.expr_stmt_tree(call_tree2, indent=0, line=5)
	
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

def print_to_number2_stmts():
	lines = []
	lines.append("PRINT-TO-NUMBER2(N)")
	lines.append("\tfor x = 0 to N")
	lines.append("\t\tif x % 2 == 0")
	lines.append("\t\t\tprint x")
	#lines.append("PRINT-TO-NUMBER(5)")
	return lines


# is_even
def check_is_even():
	"""
	IS-EVEN(N)
		return (N % 2) == 0

	IS-EVEN(4)
	"""
	bin_tree = test_utils.bin_op_val_int('N', '%', '2')

	comp_tree = Tree("COMP_EXPR")
	comp_tree.children.append(Tree("EXPR",children=[bin_tree]))
	comp_tree.children.append(test_utils.comp_operator_tree('=='))
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


def print_even_sum():
	"""
	PRINT-EVEN-SUM(x,y)
		z = x + y
		if z % 2 == 0
		 	print z
	"""

	add_tree = test_utils.add_expr("x", "y")
	assign_tree = test_utils.assign_expr_tree("z", add_tree, indent=1, line=2)

	call_tree = test_utils.call_tree("print", ["z"])
	print_tree = test_utils.expr_stmt_tree(call_tree, indent=2, line=4)

	if_tree = test_utils.if_binop_tree("z", "%", "2", "==", "0", indent=1, line=3)
	if_body = if_tree.getStmtBody()
	if_body.children.append(print_tree)

	func_tree = test_utils.func_def_tree("PRINT-EVEN-SUM", ["x", "y"])

	body_tree = func_tree.getStmtBody()
	body_tree.children.append(assign_tree)
	body_tree.children.append(Tree("STMT_LIST", indent=1, line=3, children=[if_tree]))

	prog_body = Tree("STMT_LIST", indent=0, line=0, children=[func_tree])
	return Tree("PROGRAM", children=[prog_body])

def print_even_sum_stmts():
	lines = []
	lines.append("PRINT-EVEN-SUM(x, y)")
	lines.append("\tz = x + y")
	lines.append("\tif z % 2 == 0")
	lines.append("\t\tprint z")
	return lines