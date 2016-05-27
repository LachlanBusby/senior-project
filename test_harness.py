from tree import Tree


def for_range_stmt():
	"""
	for i = 0 to 10
	"""
	# change these as needed
	indent = 1
	line = 1

	start_tree = Tree("FOR_START", children=[Tree("ASSIGN")])
	start_tree.children.append(Tree("Name", children=[Tree("i")]))
	start_tree.children.append(Tree("Assign_Op", children=[Tree("=")]))
	start_tree.children.append(Tree("EXPR",children=[Tree("Int_Literal", children=[Tree("0")])]))
	cond_tree = Tree("FOR_CONDITION",children=[Tree("For_LEQ", children=[Tree("to")])])
	end_tree = Tree("FOR_END", children=[Tree("EXPR", children=[Tree("Int_Literal",children=[Tree("10")])])])
	for_range = Tree("FOR_RANGE", children=[start_tree,cond_tree,end_tree,Tree("STMT_LIST", indent + 1, line + 1)])
	return Tree("STMT", indent, line, children=[for_range])

def while_stmt():
	"""
	while x < 10
	"""
	indent = 1
	line = 1

	expr_tree = Tree("EXPR", children = [])
	x_tree = Tree("EXPR",children=[Tree("Name", children=[Tree("x")])])
	op_tree = Tree("Comp_Op", children=[Tree("<")])
	int_tree = Tree("EXPR", children=[Tree("Int_Literal", children=[Tree("10")])])
	comp_tree = Tree("COMP_EXPR", children=[x_tree, op_tree, int_tree])

	while_tree = Tree("WHILE", children=[comp_tree, Tree("STMT_LIST", indent + 1, line + 1)])
	return Tree("STMT", indent, line, children=[while_tree])

print for_range_stmt().toString()
print "\n\n\n"
print while_stmt().toString()