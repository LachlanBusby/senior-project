from lollipop_ast import *
import collections

TAB_SIZE = 4
F = None

def get_indent(indent):
	return "".join([" "]*(indent * TAB_SIZE))

def pycode_notimplemented(self, indent):
	raise NotImplementedError("pycode method not implemented for %s" %type(self))

def register(typename):
    def decorator(func):
        dispatch[typename] = func
        return func
    return decorator


dispatch = collections.defaultdict(lambda x, y: pycode_notimplemented(x, y))

def code(node, indent):
	s = dispatch.get(type(node))(node, indent)
	#print s
#	print "Coding %s, %s: " %(type(node), node)
	return s

def emit_pycode(root, filename):
#	with f as open(filename):
#		F = f
	code_str = code(root, 0)
#	print code_str
	return code_str

@register(Statements)
def pycode_stmtlist(self, indent):
	pystr = ""
	for node in self:
		s = code(node, indent)
		pystr += get_indent(indent) + s
	return pystr

@register(Program)
def pycode_program(self, indent):
	pystr = code(self.statements, indent)
	return pystr

@register(Statement)
def pycode_stmt(self, indent):
	s = self.comment + "\n"
	if self.body is not None:
		s += code(self.body, indent + 1)
	return s


@register(FunctionDef)
def pycode_functiondef(self, indent):
	pystr = "def " + code(self.name, indent) + "("
	pystr += code(self.args, indent) + "):\n"
	pystr += code(self.body, indent + 1)
	return pystr + "\n"

@register(Arguments)
def pycode_arglist(self, indent):
	pystr = ""
	if len(self) > 0:
		pystr += code(self[0], indent)
		for arg in self[1:]:
			pystr += ", " + code(arg, indent)
	return pystr

@register(Argument)
def pycode_arg(self, indent):
	return code(self.name, indent)

@register(Assign)
def pycode_assign(self, indent):
	return code(self.target, indent) + " = " + code(self.expr, indent) + "\n"

@register(AugAssign)
def pycode_augassign(self, indent):
	pystr = code(self.target, indent) + " "
	pystr += code(self.op, indent) + "= " + code(self.expr, indent)
	return pystr + "\n"

@register(ForRange)
def pycode_forrange(self, indent):
	pystr = "for " + code(self.target, indent)
	pystr += " in range("

	#start
	if self.start != IntLiteral(0):
		pystr += code(self.start, indent) + ", " 

	#End
	pystr += code(self.end, indent)

	# increment
	if (self.inc != IntLiteral(1)):
		pystr += ", " + code(self.inc, indent)

	pystr += "):\n"
	return pystr + code(self.body, indent + 1)

@register(Foreach)
def pycode_foreach(self, indent):
	pystr = "for " + code(self.target, indent)
	pystr += " in " + code(self.iter, indent) + ":\n"
	return pystr + code(self.body, indent + 1)

@register(While)
def pycode_while(self, indent):
	pystr = "while " + code(self.test, indent) + ":\n"
	return pystr + code(self.body, indent + 1)

@register(If)
def pycode_if(self, indent):
	pystr = "if " + code(self.test, indent) + ":\n"
	pystr += code(self.body, indent + 1)
	if len(self.orelse) > 0:
		if type(self.orelse[0]) == If:
			pystr += get_indent(indent) + "el" + code(self.orelse[0], indent)
		else:
			pystr +=  get_indent(indent) + "else:\n"
			pystr +=  code(self.orelse, indent + 1)
	return pystr

@register(ExprStmt)
def pycode_exprstmt(self, indent):
	return code(self.expr, indent) + "\n"

@register(Break)
def pycode_break(self, indent):
	return "break" + "\n"

@register(Continue)
def pycode_continue(self, indent):
	return "continue" + "\n"

@register(Return)
def pycode_return(self, indent):
	return "return " + code(self.expr, indent) + "\n"

@register(Call)
def pycode_call(self, indent):	
	args = ""
	if len(self.params) > 0:
		args += code(self.params[0], indent)
		for param in self.params[1:]:
			args += ", " + code(param, indent)

	fn_name = code(self.name, indent)
	if self.name == Name("print"):
		return fn_name + " " + args 
	else:
		return fn_name + "(" + args + ")"

@register(DynamicCall)
def pycode_dynamiccall(self, indent):
	pystr = code(self.obj, indent) + "."
	pystr += code(self.fn_name, indent) + "("
	if len(self.params) > 0:
		pystr += code(self.params[0], indent)
		for param in self.params[1:]:
			pystr += ", " + code(param, indent)
	return pystr + ")"

@register(Attribute)
def pycode_attr(self, indent):
	return code(self.name, indent) + "." + code(self.attr, indent)

@register(NilExpression)
def pycode_nilexp(self, indent):
	return ""

@register(BinOp)
def pycode_binop(self, indent):
	return (code(self.left, indent) + " " +
			code(self.op, indent) + " " +
			code(self.right, indent))

@register(BoolOp)
def pycode_boolop(self, indent):
	pystr = code(self.exprs[0], indent)
	for expr in self.exprs[1:]:
		pystr += " " + code(self.op, indent) + " "
		pystr += code(expr, indent)
	return pystr

@register(UnaryOp)
def pycode_unaryop(self, indent):
	return code(self.op, indent)  +code(self.right, indent)

@register(CompareOp)
def pycode_compareop(self, indent):
	return (code(self.left, indent) + " " +
			code(self.op, indent) + " " +
			code(self.right, indent))

@register(BooleanLiteral)
@register(StringLiteral)
@register(FloatLiteral)
@register(IntLiteral)
def pycode_const(self, indent):
	return str(self.value)

@register(Name)
def pycode_name(self, indent):
	return str(self.value).replace("-", "_").lower()

@register(And)
def pycode_and(self, indent):
	return "and"

@register(Or)
def pycode_or(self, indent):
	return "or"

@register(Add)
def pycode_add(self, indent):
	return "+"

@register(Sub)
def pycode_sub(self, indent):
	return "-"

@register(Mult)
def pycode_mult(self, indent):
	return "*"

@register(Div)
def pycode_div(self, indent):
	return "/"

@register(Mod)
def pycode_mod(self, indent):
	return "%"

@register(UPlus)
def pycode_uplus(self, indent):
	return "+"

@register(UMinus)
def pycode_uminus(self, indent):
	return "-"

@register(Not)
def pycode_not(self, indent):
	return "not"

@register(Eq)
def pycode_eq(self, indent):
	return "=="

@register(Neq)
def pycode_eq(self, indent):
	return "!="

@register(Lt)
def pycode_lt(self, indent):
	return "<"

@register(Gt)
def pycode_gt(self, indent):
	return ">"

@register(Leq)
def pycode_leq(self, indent):
	return "<="

@register(Geq)
def pycode_geq(self, indent):
	return ">="

@register(Is)
def pycode_is(self, indent):
	return "is"

@register(IsNot)
def pycode_isnot(self, indent):
	return "is not"

@register(In)
def pycode_in(self, indent):
	return "in"

@register(NotIn)
def pycode_notin(self, indent):
	return "not in"