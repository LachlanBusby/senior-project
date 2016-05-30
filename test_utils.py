from tree import Tree

def return_tree(var_name):
	""" return [var_name] """
	ret_tree = Tree("RETURN", indent, line)
	ret_tree.children.append(Tree("Return_Keyword",indent,line,children=[Tree("return",indent,line)]))
	ret_tree.children.append(Tree("EXPR",indent, line, children=[Tree("Name", indent, line, children=[Tree(var_name, indent, line)])]))
	return Tree("STMT", indent, line, children=[ret_tree])

def assign_stmt_tree(var_name, var_val, var_type="Int", indent=1, line=1):
	return Tree("STMT", indent, line, children=[assign_tree(var_name, var_val, var_type, indent, line)])

def assign_tree(var_name, var_val, var_type="Int", indent=1, line=1):
	""" [var_name] = [var_val] """
	literal_nt = var_type + "_Literal"
	assign_tree = Tree("ASSIGN", indent, line)
	assign_tree.children.append(Tree("Name", indent, line, children=[Tree(var_name, indent, line)]))
	assign_tree.children.append(Tree("Assign_Op", indent, line, children=[Tree("=", indent, line)]))
	assign_tree.children.append(Tree("EXPR", indent, line, children=[Tree(literal_nt, indent, line, children=[Tree(var_val, indent, line)])]))
	return assign_tree 

def aug_assign_tree(var_name, var_val, bin_op, var_type="Int", indent=1, line=1):
	literal_nt = var_type + "_Literal"
	assign_tree = Tree("ASSIGN", indent, line)
	assign_tree.children.append(Tree("Name", indent, line, children=[Tree(var_name, indent, line)]))

	bin_nt = ""
	if bin_op == "+":
		bin_nt = Bin_Add
	elif bin_op == "-":
		bin_nt = Bin_Sub
	elif bin_op == "*":
		bin_nt = Bin_Mult
	elif bin_op == "/":
		bin_nt = Bin_Div
	elif bin_op == "%":
		bin_nt = Bin_Mod
	assign_tree.append(Tree("BIN_OP", indent, line, children=[Tree(bin_nt,indent,line,children=[Tree(bin_op,indent,line)])]))

	assign_tree.children.append(Tree("Assign_Op", indent, line, children=[Tree("=", indent, line)]))
	assign_tree.children.append(Tree("EXPR", indent, line, children=[Tree(literal_nt, indent, line, children=[Tree(var_val, indent, line)])]))
	return assign_tree 

def for_range_tree(var_name, start_val, end_val, down_to=False, by_val=None, indent=1, line=1):
	"""
	default: for [var_name] = [start_val] to [end_val]
	if down_to: for [var_name] = [start_val] downto [end_val]
	if by_val not None: for [var_name] = [start_val] to [end_val] by [by_val]
	"""
	for_range = Tree("FOR_RANGE", indent, line)
	for_range.children.append(Tree("For_Range_Keyword",indent,line,children=[Tree("for",indent,line)]))
	for_range.children.append(Tree("FOR_START", indent, line, children=[assign_tree(var_name, start_val, "Int", indent, line)]))
	
	cond_nt = "For_LEq" if not down_to else "For_GEq"
	cond_t = "to" if not down_to else "downto"
	cond_tree = Tree("FOR_CONDITION", indent, line, children=[Tree(cond_nt, indent, line, children=[Tree(cond_t, indent, line)])])
	for_range.children.append(cond_tree)

	end_tree = Tree("FOR_END", indent, line, children=[Tree("EXPR", indent, line, children=[Tree("Int_Literal",indent, line, children=[Tree(end_val, indent, line)])])])
	for_range.children.append(end_tree)

	if by_val is not None:
		op_tree = Tree("FOR_OPERATION", indent, line, children=[])
		op_tree.children.append(Tree("For_Operation_Keyword", indent, line, children=[Tree("by", indent, line)]))
		op_tree.children.append(Tree("EXPR", indent, line, children=[Tree("Int_Literal", indent, line, children=[Tree(by_val, indent, line)])]))
		for_range.children.append(op_tree)

	for_range.children.append(Tree("STMT_LIST", indent + 1, line + 1))
	return Tree("STMT", indent, line, children=[for_range])

# TODO: foreach

def while_tree(var_name, comp_op, comp_val, indent=1, line=1):
	"""
	default: while [var_name] [comp_op] [comp_val]
	"""
	comp_tree = Tree("COMP_EXPR",indent,line)
	comp_tree.children.append(Tree("EXPR",indent, line, children=[Tree("Name", indent, line, children=[Tree(var_name, indent, line)])]))

	comp_nt = ""
	if comp_op == "<":
		comp_nt = "Comp_LE"
	elif comp_op == "<=":
		comp_nt = "Comp_LEq"
	elif comp_op == ">":
		comp_nt = "Comp_GE"
	elif comp_op == ">=":
		comp_nt = "Comp_GEq"

	comp_tree.children.append(Tree("COMP_OP", indent, line, children=[Tree(comp_nt, indent, line, children=[Tree(comp_op,indent,line)])]))
	comp_tree.children.append(Tree("EXPR", indent, line, children=[Tree("Int_Literal", indent, line, children=[Tree(comp_val, indent, line)])]))

	while_tree = Tree("WHILE",indent,line,children=[])
	while_tree.children.append(Tree("While_Keyword",indent,line,children=[Tree("while",indent,line)]))
	while_tree.children.append(Tree("EXPR",indent,line,children=[comp_tree]))
	while_tree.children.append(Tree("STMT_LIST", indent + 1, line + 1)])
	return Tree("STMT", indent, line, children=[while_tree])

# TODO: else tree
def if_tree(var_name, comp_op, comp_val, indent=1, line=1):
	""" default: if [var_name] [comp_op] [comp_val] """
	comp_tree = Tree("COMP_EXPR",indent,line)
	comp_tree.children.append(Tree("EXPR",indent, line, children=[Tree("Name", indent, line, children=[Tree(var_name, indent, line)])]))

	comp_nt = ""
	if comp_op == "<":
		comp_nt = "Comp_LE"
	elif comp_op == "<=":
		comp_nt = "Comp_LEq"
	elif comp_op == ">":
		comp_nt = "Comp_GE"
	elif comp_op == ">=":
		comp_nt = "Comp_GEq"

	comp_tree.children.append(Tree("COMP_OP", indent, line, children=[Tree(comp_nt, indent, line, children=[Tree(comp_op,indent,line)])]))
	comp_tree.children.append(Tree("EXPR", indent, line, children=[Tree("Int_Literal", indent, line, children=[Tree(comp_val, indent, line)])]))

	if_tree = Tree("IF",indent,line,children=[])
	if_tree.children.append(Tree("If_Keyword",indent,line,children=[Tree("if",indent,line)]))
	if_tree.children.append(Tree("EXPR",indent,line,children=[comp_tree]))
	if_tree.children.append(Tree("STMT_LIST", indent + 1, line + 1)])
	return Tree("STMT", indent, line, children=[if_tree])

def break_tree(indent=1,line=1):
	""" break """
	break_tree = Tree("BREAK", indent, line)
	break_tree.children.append(Tree("Break_Keyword",indent,line,children=[Tree("break",indent,line)]))
	return Tree("STMT", indent, line, children=[break_tree])

def continue_tree(indent=1,line=1):
	""" continue """
	cont_tree = Tree("CONTINUE", indent, line)
	cont_tree.children.append(Tree("Continue_Keyword",indent,line,children=[Tree("continue",indent,line)]))
	return Tree("STMT", indent, line, children=[cont_tree])

	

print for_range_tree("i",0,10)
print "\n\n\n"
print while_tree("x","<",10)
