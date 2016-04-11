from astutils import SequenceMixin
from astutils import accepts

import abc
import cPickle
import StringIO
import sys

def serialize(node, filename=None):
	"""
	Serializes and saves an AST node and all its children. If 
	@filename: 	name of the file to write the serialized object to. If none, 
				function will serialize to a string.
	@ascii:		Determines whether object is serialized in binary, which is 
				much more efficient but not human-readable. 
	@return:	If filename is not None, method returns filename on
				success. Otherwise, a string containing the serialized object 
				is returned. If serialization fails for any reason, None is 
				returned
	"""
	if filename is None:
		return cPickle.dumps(node, cPickle.HIGHEST_PROTOCOL)
	else:
		try:
			outfile = open(output_filename, 'wb')
			cPickle.dump(node, outfile, cPickle.HIGHEST_PROTOCOL)
			outfile.close()
			return output_filename
		except:
			sys.stderr.write("Could not open file passed to serialize()")
			return None

def deserialize(serialized_node, isFile=False):
	"""
	Deserializes an AST object.
	@serialized_node: 	Must either be the name of a file where a serialized
						object is stored, or must be a string containing a 
						serialized object. Essentially, only pass values returned 
						from AST.serialize()
	@isFile:			If true, @serialized_node is treated as a filename, Otherwise
						its treated as a string
	"""
	if isFile:
		try:
			infile = open(serialized_node, 'rb')
			unpickled_obj = cPickle.load(infile)
			infile.close()
			return unpickled_obj
		except:
			sys.stderr.write("File passed to deserialize() could not be opened")
			return None
	else:
		return cPickle.loads(serialized_node)

# Abstract base class for all AST node classes
class AST(object):
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def __init__(self):
		pass

	def printnode(self, indent):
		string = "%s(" %self.__class__.__name__
		attributes = [(attr, val) for attr, val in vars(self).items() 
							# This disables lineno and indent level in printed trees for readability
							# Probably want at least lineno for parsing/codegen.
							if attr != 'lineno' and attr != 'indent']
		if len(attributes) > 0:
			if indent != -1:
				indentation = "\n" + "".join(["\t"]*(indent + 1))
			else:
				indentation = ""
			string += "%s=%s" %(attributes[0][0], attributes[0][1].printnode(indent + 1 if indent != -1 else -1))
			for child, value in attributes[1:]:
				string += ", %s%s=%s" %(indentation, child, value.printnode(indent + 1 if indent != -1 else -1))

		string += ")"
		return string

	def __repr__(self):
		return self.printnode(-1)


# Base sequence type for Expressions, CompareOperators, Statements and Arguments
# Sequence functionality is in SequenceMixin in astutils.py
# Supports most python functionality that built-in lists have: for-loop iteration, 
# subscripting, slices, len, get, insert, append etc.
# Note: This is an abstract class, must subclass to instantiate. 
class NodeSequence(AST, SequenceMixin):
	def printnode(self, indent):
		string = "%s([" %self.__class__.__name__ 

		if len(self._list) > 0:
			if indent != -1:
				indentation = "\n" + "".join(["\t"]*(indent + 1))
			else:
				indentation = ""			
			string += "%s%s" %(indentation, self._list[0].printnode(indent + 1 if indent != -1 else -1))
			for member in self._list:
				string += ", %s%s" %(indentation, member.printnode(indent + 1 if indent != -1 else -1))

		string += "])"
		return string

	@abc.abstractmethod
	def __init__(self, concreteType, initList):
		SequenceMixin.__init__(self, concreteType, initList)

# Base node for all Expression types
# Note, this is an abstract base class (doesn't implement __init__)
# only subclass should be explicitly instantiated
class Expression(AST):
	pass

# Sequence type for list of expressions
class Expressions(NodeSequence):
	def __init__(self, exprList):
		NodeSequence.__init__(self, Expression, exprList)


# Base class for all statement nodes
class Statement(AST):
	pass

# Node for a list of statement nodes
class Statements(NodeSequence):
	def __init__(self, stmtList):
		NodeSequence.__init__(self, Statement, stmtList)


# Root node for a parse, may change 
class Program(AST):
	@accepts(AST, Statements)
	def __init__(self, statements):
		self.statements = statements

# Base class for constant expressions
class Constant(Expression):
	def printnode(self, indent):
		return self.__class__.__name__ + "('" + str(self.value) + "')"

# Node for names 
class Name(Constant):
	@accepts(Expression, str)
	def __init__(self, token):
		self.value = token

# Float Literal
class IntLiteral(Constant):
	@accepts(Expression, int)
	def __init__(self, value):
		self.value = value

class FloatLiteral(Constant):
	@accepts(Expression, float)
	def __init__(self, value):
		self.value = value

# String Literal
class StringLiteral(Constant):
	@accepts(Expression, str)
	def __init__(self, value):
		self.value = value

# Boolean literal, True or False
class BooleanLiteral(Constant):
	@accepts(Expression, bool)
	def __init__(self, value):
		self.value = value

# Node for argument declerations in Function definitions
# Note: This is not necessary if all we want to store with each
#		argument is the name. Otherwise, we can simply make Arguments
#		a list of names
class Argument(AST):
	@accepts(AST, Name)
	def __init__(self, name):
		self.name = name

# Node for a list of argument nodes
class Arguments(NodeSequence):
	def __init__(self, argslist=None):
		NodeSequence.__init__(self, Argument, argslist)

# Node for Function Definition statements
class FunctionDef(Statement):
	@accepts(Statement, Name, Arguments, Statements)
	def __init__(self, name, arguments, body):
		self.name = name
		self.args = arguments
		self.body = body

# Node for an assignment statement. 
# Does not support:
#		arbitrary expressions on the lhs.
# 		multiple assignment, e.g. a, b = 5, 10
# Node would have to be changed to support these
class Assign(Statement):
	@accepts(Statement, Name, Expression)
	def __init__(self, target, expr):
		self.target = target
		self.expr = expr

# Binary operand base class
class BinaryOp(AST):
	def __init__(self):
		pass

# Binary operands
class Plus(BinaryOp):
	pass
class Minus(BinaryOp):
	pass
class Multiply(BinaryOp):
	pass
class Divnamee(BinaryOp):
	pass
class Modulo(BinaryOp):
	pass

# Augmented Assignment -> x += 5
class AugAssign(Statement):
	@accepts(Statement, Name, BinaryOp, Expression)
	def __init__(self, target, op, expr):
		self.target = target
		self.op = op
		self.expr = expr

# For statement in python
class Foreach(Statement):
	@accepts(Statement, Expression, Expression, Expressions)
	def __init__(self, target, iterator, body):
		self.target = target
		self.iter = iterator
		self.body = body

# While Loop node.
# does not support the Python nameiom:
# while x is True:
#	do something
# else:
# 	execute if no break occured in loop body
class While(Statement):
	@accepts(Statement, Expression, Statements)
	def __init__(self, test, body):
		self.test = test
		self.body = body

# If statement. Else or elif statements go into the orelse
# field. If no else or elif are present, orelse is an empty 
# Statements object. 
class If(Statement):
	@accepts(Statement, Expression, Statements, Statements)
	def __init__(self, test, body, orelse):
		self.test = test
		self.body = body
		self.orelse = orelse

# Node for a singleton expression, such as "fn(x)"
# or "print x"
class ExprStmt(Statement):
	@accepts(Statement, Expression)
	def __init__(self, expr):
		self.expr = expr

# Break statement
class Break(Statement):
	def __init__(self):
		pass
# Continue statement
class Continue(Statement):
	def __init__(self):
		pass

# Return statement
class Return(Statement):
	@accepts(Statement, Expression)
	def __init__(self, expr):
		self.expr = expr

# Node for a function call
# Note: does not support keyword-arguments like -> sort(cmp=myfn)
#		or sequence unpacking.	
class Call(Expression):
	@accepts(Expression, Name, Expressions)
	def __init__(self, function_name, parameters):
		self.name = function_name
		self.params = parameters


# Node for a Boolean and expression. Collapse "x and y and z" into 1 
# boolean operation with 3 expressions
class And(Expression):
	@accepts(Expression, Expressions)
	def __init__(self, expressions):
		self.exprs = expressions

# Node for a Boolean or expression.
class Or(Expression):
	@accepts(Expression, Expressions)
	def __init__(self, expressions):
		self.exprs = expressions

# Node for an addition (+) operation using
class Add(Expression):
	@accepts(Expression, Expression, Expression)
	def __init__(self, left_expr, right_expr):
		self.left = left_expr
		self.right = right_expr

# Node for a subtraction (-) operation using
class Sub(Expression):
	@accepts(Expression, Expression, Expression)
	def __init__(self, left_expr, right_expr):
		self.left = left_expr
		self.right = right_expr

# Node for a multiplication (*) operation 
class Mult(Expression):
	@accepts(Expression, Expression, Expression)
	def __init__(self, left_expr, right_expr):
		self.left = left_expr
		self.right = right_expr

# Node for a division (/) operation
class Div(Expression):
	@accepts(Expression, Expression, Expression)
	def __init__(self, left_expr, right_expr):
		self.left = left_expr
		self.right = right_expr

# Node for a modulo (%) operation
class Mod(Expression):
	@accepts(Expression, Expression, Expression)
	def __init__(self, left_expr, right_expr):
		self.left = left_expr
		self.right = right_expr

### TODO: Add binary bitwise operations

# Node for boolean unary 'not' operand
class Not(Expression):
	@accepts(Expression, Expression)
	def __init__(self, expression):
		self.expr = expression

# Node for unary minus, i.e. arithmetic negation -> 6 + (-5)
class UMinus(Expression):
	@accepts(Expression, Expression)
	def __init__(self, expression):
		self.expr = expression

# Node for unary plus, does nothing, but should be parsed for
# completeness
class UPlus(Expression):
	@accepts(Expression, Expression)
	def __init__(self, expression):
		self.expr = expression

class CompareOp(AST):
	def __init__(self):
		pass

class Eq(CompareOp):
	pass
class Lt(CompareOp):
	pass
class Gt(CompareOp):
	pass
class Leq(CompareOp):
	pass
class Geq(CompareOp):
	pass
class Is(CompareOp):
	pass
class isNot(CompareOp):
	pass
class In(CompareOp):
	pass
class NotIn(CompareOp):
	pass

class CompareOperators(NodeSequence):
	def __init__(self, opList):
		NodeSequence.__init__(self, CompareOp, opList)

# Apparently 2 < a <= b == 20 is valname Python code...
# Node for Comparator Operations. @leftmost_expr is the
# first expression, @operators is the list of comparison 
# operators from left to right and expressions is the list of
# expressions to be compared starting at the second expression
# TODO: discuss if this is the easiest way to parse this
class Compare(Expression):
	@accepts(Expression, Expression, CompareOperators, Expressions)
	def __init__(self, leftmost_expr, operators, expressions):
		self.left = leftmost_expr
		self.ops = operators
		self.exprs = expressions

'''
TODO: 
	--Short-hand if-else: "a if x < 5 else b"
	--Attribute access: "obj.attr"
	--List, set, dict comprehensions
	--List, set, dict access, lookup etc.

'''

'''
TODO: 
	Discuss choices in representing boolean, binary, unary and compare operations.

	Right now, this is what it looks like: 
	'x + y' is parsed into ===> "AddNode(left=Name('x'), right=Name('y')])"
	'x - y' is parsed into ===> "SubNode(left=Name('x'), right=Name('y')])"

	It could also be parsed like this:
	'x + y' ===> "BinOpNode(left=Name('x'), Op=Add(), right=Name('y')])"
	'x - y' ===> "BinOpNode(left=Name('x'), Op=Sub(), right=Name('y')])"

	The second is what the official python parser does. I thought the first might be 
	easier to parse.

	Boolean operations in python support chaining, so right now it looks like this:
	'x and y and z' ===> "AndNode(exprs=Expressions([Name('x'), Name('y'), Name('z')]))"
	'x or y or z' ===> "OrNode(exprs=Expressions([Name('x'), Name('y'), Name('z')]))"

	Real python doesn't parse like that, it does: BoolOp(Operator="And", Expressions=[x, y, z]).

	We could also split it up the chain into a tree like AndNode(Expr1, AndNode(Expr2, Expr3)), or not.

	I think python grammar looks like this to simplify the parsing algorithm.

	Comparison is the biggest problem. Python supports arbitrary chained expressions 
	like 5 < x < 10. This form is very psuedocode like, so we should probably support it. Formally,
	"5 < x < 10" means "5 < x" and "x < 10"

	There could be different ways of representing such a statement. I implemented what python does,
	because I figured we should talk about this. This is how python handles chained comparators:

	"5 < x < 10" ===> Compare(left=int(5), ops=[Lt(), Lt()], comparators=[Name("x"), int(10)])

	Lt() meaning less than. This is awkward, but I don't know what the easiest way to parse such an
	expression would be, so we should definitely discuss this.
'''

















