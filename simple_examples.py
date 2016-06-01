from tree import Tree
import test_utils

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

#print add_two_numbers().toString()

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

print print_to_number().toString()