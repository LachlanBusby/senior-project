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

	call_tree2 = test_utils.call_tree("fn", ["5"])
	exprstmt_tree = test_utils.expr_stmt_tree(call_tree2, line=5)
	
	prog_body = Tree("STMT_LIST", indent=0, line=0, children=[func_tree
		#, exprstmt_tree
		])
	return Tree("PROGRAM", children=[prog_body])

#print print_to_number().toString()
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
	#lines.append("fn 5")
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