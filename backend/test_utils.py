from tree import Tree
import parser_utils

### GENERAL METHODS ###

def bool_lit_tree(bool_val):
	return Tree("EXPR", children=[Tree("Int_Literal", children=[Tree(bool_val)])])

def var_tree(var_name):
	""" EXPR -> Name -> [var_name] """
	return Tree("EXPR", children=[Tree("Name", children=[Tree(var_name)])])

def add_expr(a,b):
	# op_tree = Tree("BIN_OP", children=[Tree("Bin_Add", children=[Tree("+")])])
	bin_tree = Tree("BIN_EXPR", children=[var_tree(a), bin_operator_tree("+"), var_tree(b)])
	return Tree("EXPR", children=[bin_tree])

def bin_operator_tree(bin_op):
	bin_nt = ""
	if bin_op == "+":
		bin_nt = "Bin_Add"
	elif bin_op == "-":
		bin_nt = "Bin_Sub"
	elif bin_op == "*":
		bin_nt = "Bin_Mult"
	elif bin_op == "/":
		bin_nt = "Bin_Div"
	elif bin_op == "%":
		bin_nt = "Bin_Mod"
	return Tree("BIN_OP", children=[Tree(bin_nt, children=[Tree(bin_op)])])

def bool_operator_tree(bool_op):
	bool_nt = ""
	if bool_op == "or":
		bool_nt = "Bool_Or"
	elif bool_op == "and":
		bool_nt = "Bool_And"
	return Tree("BOOL_OP", children=[Tree(bool_nt, children=[Tree(bool_op)])])

def comp_operator_tree(comp_op):
	comp_nt = ""
	if comp_op == "<":
		comp_nt = "Comp_LE"
	elif comp_op == "<=":
		comp_nt = "Comp_LEq"
	elif comp_op == ">":
		comp_nt = "Comp_GE"
	elif comp_op == ">=":
		comp_nt = "Comp_GEq"
	elif comp_op == "==":
		comp_nt = "Comp_Eq"
	elif comp_op == "!=":
		comp_nt = "Comp_NEq"
	return Tree("COMP_OP", children=[Tree(comp_nt, children=[Tree(comp_op)])])

def boolop_tree(expr1, op, expr2):
	return Tree("EXPR", children=[Tree("BOOL_EXPR", children=[expr1, bool_operator_tree(op), expr2])])

def binop_tree(expr1, op, expr2):
	return Tree("EXPR", children=[Tree("BIN_OP", children=[expr1, bin_operator_tree(op), expr2])])

def compop_tree(expr1, op, expr2):
	return Tree("EXPR", children=[Tree("COMP_OP", children=[expr1, comp_operator_tree(op), expr2])])

def comp_op_val_int(var, op, intlit):
	comp_tree = Tree("COMP_EXPR", children=[var_tree(var), comp_operator_tree(op), int_lit_tree(intlit)])
	return Tree("EXPR", children=[comp_tree])

def bin_op_val_int(var, op, intlit):
	bin_tree = Tree("BIN_EXPR", children=[var_tree(var), bin_operator_tree(op), int_lit_tree(intlit)])
	return Tree("EXPR", children=[bin_tree])

def name_tree(var_name):
	return Tree("Name", children=[Tree(var_name)])

def arg_tree(arg_name):
	return Tree("ARG",children=[var_tree(arg_name)])

def int_lit_tree(lit_val):
	return Tree("EXPR", children=[Tree("Int_Literal",children=[Tree(lit_val)])])

def call_tree(func_name, args=None, expr_args=False, parens=False):
	call = Tree("CALL")
	call.children.append(Tree("Func_Name", children=[Tree(func_name)]))
	if parens:
		call.children.append(Tree("Open_Paren", children=[Tree('(')]))
	if args is not None:
		exprs = args if expr_args else [var_tree(a) for a in args]
		call.children.append(expr_list_tree(exprs))

	if parens:
		call.children.append(Tree("Close_Paren", children=[Tree(')')]))
	return Tree("EXPR", children=[call])

def expr_list_tree(expr_trees):
	list_tree = Tree("EXPR_LIST")
	curr_list = list_tree
	for enum, e in enumerate(expr_trees):
		if len(curr_list.children) >= 1:
			curr_list.children.append(Tree("LIST_DELIM", children=[Tree("Comma", children=[Tree(",")])]))
			new_list = Tree("EXPR_LIST")
			curr_list.children.append(new_list)
			curr_list = new_list
		curr_list.children.append(e)
	return list_tree


### STATEMENT SPECIFIC ###

def func_def_tree(func_name, args=None, indent=0, line=1):
	""" default: FUNC-NAME(args)"""
	def_tree = Tree("FUNC_DEF", children=[])
	def_tree.children.append(Tree("Func_Name", children=[Tree(func_name)]))
	def_tree.children.append(Tree("Open_Paren", children=[Tree('(')]))
	if args is not None:
		def_tree.children.append(arg_list_tree(args))
	def_tree.children.append(Tree("Close_Paren", children=[Tree(')')]))
	def_tree.children.append(Tree("STMT_LIST", indent + 1, line + 1))
	return Tree("STMT", indent, line, children=[def_tree])
	
def arg_list_tree(args):
	list_tree = Tree("ARG_LIST")
	curr_list = list_tree
	for anum, a in enumerate(args):
		if len(curr_list.children) >= 1:
			curr_list.children.append(Tree("LIST_DELIM", children=[Tree("Comma", children=[Tree(",")])]))
			new_list = Tree("ARG_LIST")
			curr_list.children.append(new_list)
			curr_list = new_list
		curr_list.children.append(Tree("ARG", children=[var_tree(a)]))
	return list_tree

def return_tree(var_name, indent=0, line=1):
	""" return [var_name] """
	ret_tree = Tree("RETURN")
	ret_tree.children.append(Tree("Return_Keyword",children=[Tree("return")]))
	ret_tree.children.append(var_tree(var_name))
	return Tree("STMT", indent, line, children=[ret_tree])

def return_val_tree(val, indent=0, line=1):
	""" return [val] """
	ret_tree = Tree("RETURN")
	ret_tree.children.append(Tree("Return_Keyword", children=[Tree("return")]))
	ret_tree.children.append(int_lit_tree(val))
	return Tree("STMT", indent, line, children=[ret_tree])

def return_expr_tree(ret_expr, indent=0, line=1):
	""" return [var_name] """
	ret_tree = Tree("RETURN")
	ret_tree.children.append(Tree("Return_Keyword",children=[Tree("return")]))
	ret_tree.children.append(ret_expr)
	return Tree("STMT", indent, line, children=[ret_tree])

def assign_stmt_tree(var_name, var_val, var_type="Int", indent=0, line=1):
	return Tree("STMT", indent, line, children=[assign_tree(var_name, var_val, var_type)])

def assign_expr_tree(var_name, val_tree, indent=0, line=1, as_stmt=True):
	assign_tree = Tree("ASSIGN")
	assign_tree.children.append(Tree("Name", children=[Tree(var_name)]))
	assign_tree.children.append(Tree("Assign_Op", children=[Tree("=")]))
	assign_tree.children.append(val_tree)
	if as_stmt:
		return Tree("STMT", indent, line, children=[assign_tree])
	else:
		return assign_tree

def assign_tree(var_name, var_val, var_type="Int"):
	""" [var_name] = [var_val] """
	literal_nt = var_type + "_Literal"
	assign_tree = Tree("ASSIGN")
	assign_tree.children.append(name_tree)
	assign_tree.children.append(Tree("Assign_Op", children=[Tree("=")]))
	assign_tree.children.append(Tree("EXPR", children=[Tree(literal_nt, children=[Tree(var_val)])]))
	return assign_tree 

def aug_assign_tree(var_name, var_val, bin_op, var_type="Int", indent=0, line=1):
	literal_nt = var_type + "_Literal"
	assign_tree = Tree("AUG_ASSIGN")
	assign_tree.children.append(Tree("Name", children=[Tree(var_name)]))

	assign_tree.children.append(bin_operator_tree(bin_op))

	assign_tree.children.append(Tree("Assign_Op", children=[Tree("=")]))
	assign_tree.children.append(Tree("EXPR", children=[Tree(literal_nt, children=[Tree(var_val)])]))
	return Tree("STMT", indent, line, children=[assign_tree])

def aug_assign_expr_tree(var_name, val_tree, indent=0, line=1, as_stmt=True):
	assign_tree = Tree("AUG_ASSIGN")
	assign_tree.children.append(Tree("Name", children=[Tree(var_name)]))
	assign_tree.children.append(Tree("Assign_Op", children=[Tree("=")]))
	assign_tree.children.append(val_tree)
	if as_stmt:
		return Tree("STMT", indent, line, children=[assign_tree])
	else:
		return assign_tree

def for_range_tree(var_name, start_expr, end_expr, down_to=False, by_val=None, indent=0, line=1):
	"""
	default: for [var_name] = [start_val] to [end_val]
	if down_to: for [var_name] = [start_val] downto [end_val]
	if by_val not None: for [var_name] = [start_val] to [end_val] by [by_val]
	"""
	for_range = Tree("FOR_RANGE")
	for_range.children.append(Tree("For_Range_Keyword",children=[Tree("for")]))
	for_range.children.append(Tree("FOR_START", children=[assign_expr_tree(var_name, start_expr, as_stmt=False)]))
	
	cond_nt = "For_LEq" if not down_to else "For_GEq"
	cond_t = "to" if not down_to else "downto"
	cond_tree = Tree("FOR_CONDITION", children=[Tree(cond_nt, children=[Tree(cond_t)])])
	for_range.children.append(cond_tree)

	end_tree = Tree("FOR_END", children=[end_expr])
	for_range.children.append(end_tree)

	if by_val is not None:
		op_tree = Tree("FOR_OPERATION", children=[])
		op_tree.children.append(Tree("For_Operation_Keyword", children=[Tree("by")]))
		op_tree.children.append(Tree("EXPR", children=[Tree("Int_Literal", children=[Tree(by_val)])]))
		for_range.children.append(op_tree)

	for_range.children.append(Tree("STMT_LIST", indent + 1, line + 1))
	return Tree("STMT", indent, line, children=[for_range])

# TODO: foreach

def while_tree(var_name, comp_op, comp_val, indent=0, line=1):
	"""
	default: while [var_name] [comp_op] [comp_val]
	"""
	comp_tree = Tree("COMP_EXPR")
	comp_tree.children.append(Tree("EXPR",children=[Tree("Name", children=[Tree(var_name)])]))

	comp_tree.children.append(comp_operator_tree(comp_op))
	comp_tree.children.append(Tree("EXPR", children=[Tree("Int_Literal", children=[Tree(comp_val)])]))

	while_tree = Tree("WHILE",children=[])
	while_tree.children.append(Tree("While_Keyword",children=[Tree("while")]))
	while_tree.children.append(Tree("EXPR",children=[comp_tree]))
	while_tree.children.append(Tree("STMT_LIST", indent + 1, line + 1))
	return Tree("STMT", indent, line, children=[while_tree])

def if_binop_tree(var_name, bin_op, intval, comp_op, compval, indent=0, line=1):
	comp_tree = Tree("COMP_EXPR", children=[
					Tree("BIN_EXPR", children=[
						name_tree(var_name), 
						bin_operator_tree(bin_op), 
						int_lit_tree(intval)]),
					comp_operator_tree(comp_op), 
					Tree("EXPR",children=[Tree("Int_Literal", children=[Tree(compval)])])])

	if_tree = Tree("IF",children=[])
	if_tree.children.append(Tree("If_Keyword",children=[Tree("if")]))
	if_tree.children.append(Tree("EXPR",children=[comp_tree]))
	if_tree.children.append(Tree("STMT_LIST", indent + 1, line + 1))
	return Tree("STMT", indent, line, children=[if_tree])

# TODO: else tree

def if_expr_tree(cond_expr, indent=0, line=1):
	""" default: if [var_name] [comp_op] [comp_val] """
	if_tree = Tree("IF",children=[])
	if_tree.children.append(Tree("If_Keyword",children=[Tree("if")]))
	if_tree.children.append(Tree("EXPR",children=[cond_expr]))
	if_tree.children.append(Tree("STMT_LIST", indent + 1, line + 1))
	return Tree("STMT", indent, line, children=[if_tree])

def if_tree(var_name, comp_op, comp_val, indent=0, line=1):
	""" default: if [var_name] [comp_op] [comp_val] """
	comp_tree = Tree("COMP_EXPR")
	comp_tree.children.append(Tree("EXPR",children=[Tree("Name",children=[Tree(var_name)])]))

	comp_tree.children.append(comp_operator_tree(comp_op))
	comp_tree.children.append(Tree("EXPR",children=[Tree("Int_Literal", children=[Tree(comp_val)])]))

	if_tree = Tree("IF",children=[])
	if_tree.children.append(Tree("If_Keyword",children=[Tree("if")]))
	if_tree.children.append(Tree("EXPR",children=[comp_tree]))
	if_tree.children.append(Tree("STMT_LIST", indent + 1, line + 1))
	return Tree("STMT", indent, line, children=[if_tree])

def break_tree(indent=0,line=1):
	""" break """
	break_tree = Tree("BREAK")
	break_tree.children.append(Tree("Break_Keyword",children=[Tree("break")]))
	return Tree("STMT", indent, line, children=[break_tree])

def continue_tree(indent=0,line=1):
	""" continue """
	cont_tree = Tree("CONTINUE")
	cont_tree.children.append(Tree("Continue_Keyword", children=[Tree("continue")]))
	return Tree("STMT", indent, line, children=[cont_tree])

def expr_stmt_tree(expr, indent=0, line=1):
	return Tree("STMT", indent, line, children=[Tree("EXPR_STMT", indent, line, children=[expr])])

#print func_def_tree("TESTING").toString()
#print func_def_tree("TESTING", ["a", "b"]).toString()
#print arg_list_tree(["a", "b"]).toString()
#print assign_stmt_tree("x", "2").toString()
#print for_range_tree("i", "0", "10").toString()

# productions = {stmt_type: [] for stmt_type in parser_utils.STMT_TYPES}
# parser_utils.stmt_prods(if_tree("x", "<", "10"), productions)
# for p in productions:
# 	p_strs = []
# 	for r in productions[p]:
# 		p_strs.append(r.unicode_repr())
# 	print p + " : [" + "; ".join(p_strs) + "]"
