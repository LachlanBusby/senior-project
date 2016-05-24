from tree import Tree


def for_range_stmt():
	"""
	for i = 0 to 10
	"""
	# change these as needed
	indent = 1
	line = 1

	start_tree = Tree("FOR_START", indent, line, children=[Tree("ASSIGN", indent, line)])
	start_tree.children.append(Tree("Name", indent, line, children=[Tree("i", indent, line)]))
	start_tree.children.append(Tree("Assign_Op", indent, line, children=[Tree("=", indent, line)]))
	start_tree.children.append(Tree("EXPR", indent, line, children=[Tree("Int_Literal", indent, line, children=[Tree("0", indent, line, )])]))
	cond_tree = Tree("FOR_CONDITION", indent, line, children=[Tree("For_LEQ", indent, line, children=[Tree("to", indent, line)])])
	end_tree = Tree("FOR_END", indent, line, children=[Tree("EXPR", indent, line, children=[Tree("Int_Literal",indent, line, children=[Tree("10", indent, line)])])])
	for_range = Tree("FOR_RANGE", indent, line, children=[start_tree,cond_tree,end_tree,Tree("STMT_LIST", indent + 1, line + 1)])
	return Tree("STMT", indent, line, children=[for_range])

def while_stmt():
	"""
	while x < 10
	"""
	indent = 1
	line = 1

	expr_tree = Tree("EXPR", indent, line, children = [])
	x_tree = Tree("EXPR",indent, line, children=[Tree("Name", indent, line, children=[Tree("x", indent, line)])])
	op_tree = Tree("Comp_Op", indent, line, children=[Tree("<", indent, line)])
	int_tree = Tree("EXPR", indent, line, children=[Tree("Int_Literal", indent, line, children=[Tree("10", indent, line)])])
	comp_tree = Tree("COMP_EXPR", indent, line, children=[x_tree, op_tree, int_tree])

	while_tree = Tree("WHILE", indent, line, children=[comp_tree, Tree("STMT_LIST", indent + 1, line + 1)])
	return Tree("STMT", indent, line, children=[while_tree])

print for_range_stmt().toString()
print "\n\n\n"
print while_stmt().toString()