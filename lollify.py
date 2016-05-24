from lollipop_ast import *
from tree import Tree
import collections

TAB_SIZE = 4
F = None

def lollify_notimplemented(node):
	raise NotImplementedError("lollify method not implemented for %s" %(node.label))

dispatch = collections.defaultdict(lambda x: lollify_notimplemented(x))

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
		return [children[label]]
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

@register("STMT")
def lollify_stmtlist(node):
	return lollify(node.children[0])

@register("EXPR")
def lollify_stmtlist(node):
	return lollify(node.children[0])

@register("STMT_LIST")
def lollify_stmtlist(node):
	stmts = extract_list_children("STMT", "STMT_LIST")
	return Statements([lollify(stmt) for stmt in stmts])

@register("PROGRAM")
def lollify_program(node):
	return Program(lollify(node.children[0]))

@register("FUNC_DEF")
def lollify_functiondef(node):
	children = get_child_dict(node)
	return FunctionDef(lollify(children["Func_Name"]),
					   lollify(children["ARG_LIST"],
					   lollify(children["STMT_LIST"])))

@register("ARG_LIST")
def lollify_arglist(node):
	args = extract_list_children("ARG", "ARG_LIST")
	return Arguments([lollify(arg) for arg in args])

@register("ARG")
def lollify_arg(node):
	return lollify(node.children[0])

@register("ASSIGN")
def lollify_assign(node):
	children = get_child_dict(node)
	return Assign(lollify(children["Name"]), lollify(children["EXPR"]))

@register("AUG_ASSIGN")
def lollify_augassign(node):
	children = get_child_dict(node)
	return Assign(lollify(children["Name"]),
				  lollify(children["Bin_Op"]),
				  lollify(children["EXPR"]))

@register("FOR_START")
def lollify_forstart(node):
	children = get_child_dict(node)
	return lollify(children["Name"]), lollify(children["EXPR"])

@register("FOR_END")
def lollify_forstart(node):
	children = get_child_dict(node)
	return lollify(children["EXPR"])

@register("FOR_RANGE")
def lollify_forrange(node):
	children = get_child_dict(node)
	target, start = lollify(children["FOR_START"])
	return ForRange(target, 
					start, 
					lollify(children["FOR_END"]),
					IntLiteral(1) # Hard coding increment for now, not sure which child has this info
					lollify(children["STMT_LIST"]))

@register("FOR_END")
def lollify_forstart(node):
	children = get_child_dict(node)
	return lollify(children["EXPR"])

@register(Foreach)
def lollify_foreach(node):
	pass

@register("WHILE")
def lollify_while(node):
	return While(lollify(node.children[1],
				 lollify(node.children[2])))

@register(If)
def lollify_if(node):
	pass

@register(ExprStmt)
def lollify_exprstmt(node):
	pass

@register(Break)
def lollify_break(node):
	pass

@register(Continue)
def lollify_continue(node):
	pass

@register(Return)
def lollify_return(node):
	pass

@register(Call)
def lollify_call(node):
	pass

@register(DynamicCall)
def lollify_dynamiccall(node):
	pass

@register(Attribute)
def lollify_attr(node):
	pass

@register("BIN_OP")
def lollify_binop(node):
	children = get_child_dict(node)
	return BinOp(lollify(children["LEFT_EXPR"]), 
				 lollify(children["Bin_Op"],
				 lollify(children["RIGHT_EXPR"])))

@register("Bin_Op")
def lollify_binoperator(node):
	return lollify(node.children[0])

@register(BoolOp)
def lollify_boolop(node):
	pass

@register(UnaryOp)
def lollify_unaryop(node):
	pass

@register(CompareOp)
def lollify_compareop(node):
	pass

@register(And)
def lollify_and(node):
	pass

@register(Or)
def lollify_or(node):
	pass

@register("+")
def lollify_add(node):
	return Add()

@register("-")
def lollify_sub(node):
	return Sub()

@register("*")
def lollify_mult(node):
	return Mult()

@register("/")
def lollify_div(node):
	return Div()

@register("%")
def lollify_mod(node):
	return Mod()

@register(UPlus)
def lollify_uplus(node):
	pass

@register(UMinus)
def lollify_uminus(node):
	pass

@register(Not)
def lollify_not(node):
	pass

@register(Eq)
def lollify_eq(node):
	pass

@register(Lt)
def lollify_lt(node):
	pass

@register(Gt)
def lollify_gt(node):
	pass

@register(Leq)
def lollify_leq(node):
	pass

@register(Geq)
def lollify_geq(node):
	pass

@register(Is)
def lollify_is(node):
	pass

@register(IsNot)
def lollify_isnot(node):
	pass

@register(In)
def lollify_in(node):
	pass

@register(NotIn)
def lollify_notin(node):
	pass