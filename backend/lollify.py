from lollipop_ast import *
from astutils import register
from tree import Tree
import collections

TAB_SIZE = 4
F = None

def lollify_notimplemented(node):
	raise NotImplementedError("lollify method not implemented for %s" %(node.label))

def register(typename):
    def decorator(func):
        dispatch[typename] = func
        return func
    return decorator

def register_extractor(listtype):
    def decorator(func):
        list_extractor[listtype] = func
        return func
    return decorator

dispatch = collections.defaultdict(lambda x: lollify_notimplemented(x))
list_extractor = collections.defaultdict(lambda x: lollify_notimplemented(x))

@register_extractor("EXPR_LIST")
def extract_exprlist(node):
	return extract_list_children(node, "EXPR", "EXPR_LIST")

@register_extractor("STMT_LIST")
def extract_stmtlist(node):
	return extract_list_children(node, "STMT", "STMT_LIST")

@register_extractor("ARG_LIST")
def extract_arglist(node):
	return extract_list_children(node, "ARG", "ARG_LIST")

def extract_children(node):
	return list_extractor[node.label](node)

def get_child_dict(node):
	"""
	This will break if called with a node that has children with same label.
	Uses a dict comprehension
	"""
	assert(max(collections.Counter([child.label for child in node.children])) > 1), "Conversion to child dictionary failed due to label collsion"
	return {child.label : child for child in node.children}

def extract_list_children(node, label, list_label):
	"""
	Recursively extract list of <label> nodes from a <list_label> node.
	This makes the main recursive traversal simpler.
	"""
	children = get_child_dict(node)
	if children.get(list_label) is None:
		return [] if children.get(label) is None else [children[label]]
	else:
		return [children[label]] + extract_list_children(children[list_label], label, list_label)

def lollify(node):
	"""
	Main dispatch method, eliminates the need for a if-else chain or baking this 
	into the tree class definition
	"""
	return dispatch.get(node.label)(node)

def lollify_root(root):
	"""
	Clients should use this method to convert tree into AST
	"""
	return lollify(root)

@register("Error_Line")
def lollify_error(node):
	return node.children[0].label

@register("ERROR")
def lollify_error(node):
	children = get_child_dict(node)
	stmt = Statement(lollify(children["Error_Line"]))
	if children.get("STMT_LIST") is not None:
		stmt.body = lollify(children["STMT_LIST"])
	return stmt

@register("STMT")
def lollify_stmt(node):
	children = get_child_dict(node)
	if children.get("ERROR") is not None:
		return lollify(children["ERROR"])
	return lollify(node.children[0])

@register("EXPR")
def lollify_expr(node):
	return lollify(node.children[0])

@register("STMT_LIST")
def lollify_stmtlist(node):
	stmts = extract_children(node)
	return Statements([lollify(stmt) for stmt in stmts])

@register("EXPR_LIST")
def lollify_stmtlist(node):
	stmts = extract_children(node)
	return Expressions([lollify(stmt) for stmt in stmts])

@register("PROGRAM")
def lollify_program(node):
	return Program(lollify(node.children[0]))

@register("FUNC_DEF")
def lollify_functiondef(node):
	children = get_child_dict(node)
	return FunctionDef(lollify(children["Func_Name"]),
					   lollify(children["ARG_LIST"]),
					   lollify(children["STMT_LIST"]))

@register("ARG_LIST")
def lollify_arglist(node):
	args = extract_children(node)
	return Arguments([lollify(arg) for arg in args])

@register("ARG")
def lollify_arg(node):
	return Argument(lollify(node.children[0]))

@register("ASSIGN")
def lollify_assign(node):
	children = get_child_dict(node)
	return Assign(lollify(children["Name"]), lollify(children["EXPR"]))

@register("AUG_ASSIGN")
def lollify_augassign(node):
	children = get_child_dict(node)
	return AugAssign(lollify(children["Name"]),
					 lollify(children["BIN_OP"]),
					 lollify(children["EXPR"]))

@register("FOR_START")
def lollify_forstart(node):
	if node.children[0].label == "ASSIGN":
		children = get_child_dict(node.children[0])
		return lollify(children["Name"]), lollify(children["EXPR"])
	elif node.children[0].label == "EXPR":
		return lollify(node.children[0])

@register("FOR_END")
def lollify_forend(node):
	children = get_child_dict(node)
	return lollify(children["EXPR"])

@register("FOR_OPERATION")
def lollify_forop(node):
	children = get_child_dict(node)
	return lollify(children["EXPR"])

@register("FOR_RANGE")
def lollify_forrange(node):
	children = get_child_dict(node)
	target, start = lollify(children["FOR_START"])
	return ForRange(target, 
					start, 
					lollify(children["FOR_END"]),
					IntLiteral(1) if children.get("FOR_OPERATION") is None else lollify(children["FOR_OPERATION"]),
					lollify(children["STMT_LIST"]))

@register("FOR_END")
def lollify_forstart(node):
	children = get_child_dict(node)
	return lollify(children["EXPR"])

@register("FOR_EACH")
def lollify_foreach(node):
	raise NotImplementedError()

@register("WHILE")
def lollify_while(node):
	children = get_child_dict(node)
	return While(lollify(children["EXPR"]),
				 lollify(children["STMT_LIST"]))

@register("ELSE")
def lollify_else(node):
	children = get_child_dict(node)
	if children.get("STMT_LIST") is not None:
		return lollify(children["STMT_LIST"])
	else:
		return Statements([])

@register("ELSE_IF")
def lollify_elseif(node):
	children = get_child_dict(node)
	if children.get("IF") is not None:
		return lollify(children["IF"])
	else:
		return lollify_if(node)

@register("IF")
def lollify_if(node):
	children = get_child_dict(node)
	else_if = None
	if children.get("ELSE_IF") is not None:
		else_if = lollify(children["ELSE_IF"])
	elif children.get("ELSE") is not None:
		else_if = lollify(children["ELSE_IF"])
	else:
		else_if = Statements([])
	return If(lollify(children["EXPR"]), 
		      lollify(children["STMT_LIST"]), 
			   else_if)

@register("EXPR_STMT")
def lollify_exprstmt(node):
	children = get_child_dict(node)
	return ExprStmt(lollify(children["EXPR"]))

@register("BREAK")
def lollify_break(node):
	return Break()

@register("CONTINUE")
def lollify_continue(node):
	return Continue()

@register("RETURN")
def lollify_return(node):
	if len(node.children) > 0:
		return Return(lollify(node.children[1]))
	else:
		return Return(NilExpression())

@register("CALL")
def lollify_call(node):
	children = get_child_dict(node)
	return Call(lollify(children["Func_Name"]), lollify(children["EXPR_LIST"]))

'''
@register(DynamicCall)
def lollify_dynamiccall(node):
	raise NotImplementedError()

@register(Attribute)
def lollify_attr(node):
	raise NotImplementedError()
'''

@register("Func_Name")
@register("Name")
def lollify_name(node):
	return Name(node.children[0].label)

@register("Int_Literal")
def lollify_intliteral(node):
	return IntLiteral(int(node.children[0].label))

@register("Float_Literal")
def lollify_floatliteral(node):
	return FloatLiteral(float(node.children[0].label))

@register("Bool_Literal")
def lollify_boolliteral(node):
	return BooleanLiteral(node.children[0].label == "true")

@register("String_Literal")
def lollify_boolliteral(node):
	return StringLiteral(node.children[0].label)

@register("BIN_EXPR")
def lollify_binop(node):
	return BinOp(lollify(node.children[0]), 
				 lollify(node.children[1]),
				 lollify(node.children[2]))



@register("BOOL_EXPR")
def lollify_boolop(node):
	return BinOp(lollify(node.children[0]), 
				 lollify(node.children[1]),
				 lollify(node.children[2]))

@register("UNARY_EXPR")
def lollify_unaryop(node):
	return UnaryOp(lollify(node.children[0]), 
				 lollify(node.children[1]))

@register("COMP_EXPR")
def lollify_compareop(node):
	return CompareOp(lollify(node.children[0]), 
				 	 lollify(node.children[1]),
				 	 lollify(node.children[2]))

@register("BIN_OP")
@register("Bin_Op")
def lollify_binoperator(node):
	return lollify(node.children[0])

@register("BOOL_OP")
def lollify_booloperator(node):
	return lollify(node.children[0])

@register("COMP_OP")
def lollify_compoperator(node):
	return lollify(node.children[0])

@register("UNARY_OP")
def lollify_unaryoperator(node):
	return lollify(node.children[0])

@register("Bool_And")
def lollify_and(node):
	return And()

@register("Bool_Or")
def lollify_or(node):
	return Or()

@register("Bin_Add")
def lollify_add(node):
	return Add()

@register("Bin_Sub")
def lollify_sub(node):
	return Sub()

@register("Bin_Mult")
def lollify_mult(node):
	return Mult()

@register("Bin_Div")
def lollify_div(node):
	return Div()

@register("Bin_Mod")
def lollify_mod(node):
	return Mod()

@register("Unary_Plus")
def lollify_uplus(node):
	return UPlus()

@register("Unary_Minus")
def lollify_uminus(node):
	return UMinus()

@register("Not")
def lollify_not(node):
	return Not()

@register("Comp_Eq")
def lollify_eq(node):
	return Eq()

@register("Comp_NEq")
def lollify_neq(node):
	return Neq()

@register("Comp_LE")
def lollify_le(node):
	return Lt()

@register("Comp_GE")
def lollify_ge(node):
	return Gt()

@register("Comp_LEq")
def lollify_leq(node):
	return Leq()

@register("Comp_GEq")
def lollify_geq(node):
	return Geq()

@register("Comp_Is")
def lollify_is(node):
	return Is()

@register("Comp_IsNot")
def lollify_isnot(node):
	return IsNot()

@register("Comp_In")
def lollify_in(node):
	return In()

@register("Comp_NotIn")
def lollify_notin(node):
	return NotIn()