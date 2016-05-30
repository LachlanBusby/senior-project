from astutils import SequenceMixin
from astutils import accepts

import abc
import cPickle
import StringIO
import sys

PRINT_WITH_NEWLINE = True

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

class AST(object):
	"""
	Abstract base class for all AST node classes. Implements 
	automatic python printing for all nodes. 
	"""
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def __init__(self):
		self.lineno = None
		self.indent = None
		pass

	def printnode(self, indent):
		string = "%s(" %self.__class__.__name__
		attributes = [(attr, val) for attr, val in vars(self).items() 
							# This disables lineno and indent level in printed trees for readability
							# Probably want at least lineno for parsing/codegen.
							if attr != 'lineno' and attr != 'indent']
		if len(attributes) > 1:
			if PRINT_WITH_NEWLINE:
				indentation = indent + "".join([" "]*4)
			else:
				indentation = ""
			string += "%s%s=%s" %("\n" + indentation, attributes[0][0], attributes[0][1].printnode(indentation))
			for child, value in attributes[1:]:
				string += ", %s%s=%s" %("\n" + indentation, child, value.printnode(indentation))
		elif len(attributes) == 1:
				string += "%s%s=%s" %("", attributes[0][0], attributes[0][1].printnode(indent + "".join([" "]*8)))
		string += ")"
		return string

	def __repr__(self):
		return self.printnode("")

class NodeSequence(AST, SequenceMixin):
	"""
	Base sequence type for Expressions, CompareOperators, Statements and Arguments
	Sequence functionality is in SequenceMixin in astutils.py
	Supports most python functionality that built-in lists have: for-loop iteration, 
	subscripting, slices, len, get, insert, append etc.
	Note: This is an abstract class, must subclass to instantiate.
	"""
	def printnode(self, indent):
		string = "%s([" %self.__class__.__name__ 

		if len(self._list) > 0:
			if indent != -1:
				indentation = indent + "".join([" "]*4)
			else:
				indentation = ""
			string += "%s%s" %("\n" + indentation, self._list[0].printnode(indentation))
			for member in self._list[1:]:
				string += ", %s%s" %("\n" + indentation, member.printnode(indentation))

		string += "])"
		return string

	@abc.abstractmethod
	def __init__(self, concreteType, initList):
		SequenceMixin.__init__(self, concreteType, initList)

class Expression(AST):
	"""	
	Base node for all Expression types
	Note, this is an abstract base class (doesn't implement __init__)	
	only subclasses should be explicitly instantiated
	"""
	pass

class Statement(AST):
	""" Base class for all statement nodes """
	pass

class Operator(AST):
	""" Base Operator class. Do not instantiate """
	pass
class BooleanOperator(Operator):
	""" Base class for 'And' and 'Or' operators """
	pass
class BinaryOperator(Operator):
	""" Base class for Add, Sub, Mult, Div and Mod """
	pass
class UnaryOperator(Operator):
	""" Base class for UPlus, UMinus, Not """
	pass
class CompareOperator(Operator):
	""" Base class for all comparators """
	pass

class Expressions(NodeSequence):
	""" Sequence type for list of expressions """
	def __init__(self, exprList):
		NodeSequence.__init__(self, Expression, exprList)

class Statements(NodeSequence):
	""" Sequence type for list of statements """
	def __init__(self, stmtList):
		NodeSequence.__init__(self, Statement, stmtList)

class Program(AST):
	""" Root node for a parse, may change """
	@accepts(AST, Statements)
	def __init__(self, statements):
		self.statements = statements

class Constant(Expression):
	""" Base class for constant expressions """
	def printnode(self, indent):
		return self.__class__.__name__ + "('" + str(self.value) + "')"

class Name(Constant):
	"""
	Node for names 
	"""
	@accepts(Expression, str)
	def __init__(self, token):
		self.value = token

class Argument(AST):
	"""
	Node for argument declerations in Function definitions
	Note: This is not necessary if all we want to store with each
		argument is the name. Otherwise, we can simply make Arguments
		a list of names
	"""
	@accepts(AST, Name)
	def __init__(self, name):
		self.name = name

class Arguments(NodeSequence):
	""" Sequence node for a list of argument nodes """
	def __init__(self, argslist=None):
		NodeSequence.__init__(self, Argument, argslist)

# 
class FunctionDef(Statement):
	""" Node for Function Definition statements """
	@accepts(Statement, Name, Arguments, Statements)
	def __init__(self, name, arguments, body):
		self.name = name
		self.args = arguments
		self.body = body

class Assign(Statement):
	"""
	Node for an assignment statement. 
	Does not support:
		arbitrary expressions on the lhs.
		multiple assignment, e.g. a, b = 5, 10
	Node would have to be changed to support these
	"""
	@accepts(Statement, Name, Expression)
	def __init__(self, target, expr):
		self.target = target
		self.expr = expr

class AugAssign(Statement):
	""" Augmented Assignment -> x += 5 """
	@accepts(Statement, Name, BinaryOperator, Expression)
	def __init__(self, target, op, expr):
		self.target = target
		self.op = op
		self.expr = expr

class ForRange(Statement):
	""" Range-based, C-style loop """
	@accepts(Statement, Expression, Expression, Expression, Expression, Statements)
	def __init__(self, target, start, end, increment, body):
		self.target = target
		self.start = start
		self.end = end
		self.inc = increment
		self.body = body

class Foreach(Statement):
	""" For statement in python """
	@accepts(Statement, Expression, Expression, Expressions)
	def __init__(self, target, iterator, body):
		self.target = target
		self.iter = iterator
		self.body = body

class While(Statement):
	"""
	While Loop node.
	does not support the Python idiom:
	while x is True:
		do something
	else:
		execute if no break occured in loop body
	"""
	@accepts(Statement, Expression, Statements)
	def __init__(self, test, body):
		self.test = test
		self.body = body

class If(Statement):
	"""
	If statement. Else or elif statements go into the orelse
	field. If no else or elif are present, orelse is an empty 
	Statements object. 
	"""
	@accepts(Statement, Expression, Statements, Statements)
	def __init__(self, test, body, orelse):
		self.test = test
		self.body = body
		self.orelse = orelse

class ExprStmt(Statement):
	"""
	Node for a singleton expression, such as "fn(x)"
	or "print x"
	"""
	@accepts(Statement, Expression)
	def __init__(self, expr):
		self.expr = expr

class Break(Statement):
	""" Break statement """
	def __init__(self):
		pass

class Continue(Statement):
	""" Continue statement """
	def __init__(self):
		pass

class Return(Statement):
	""" Return statement """
	@accepts(Statement, Expression)
	def __init__(self, expr):
		self.expr = expr

class Call(Expression):
	"""
	Node for a function call
	Note: 	does not support keyword-arguments like -> sort(cmp=myfn)
			or sequence unpacking.	
	"""
	@accepts(Expression, Name, Expressions)
	def __init__(self, function_name, parameters):
		self.name = function_name
		self.params = parameters

class DynamicCall(Expression):
	"""
	Node for a function call like x.foo(arg)
	Ideally supports stuff like bar().foo() where bar() returns an instance
	with a class method foo(). But instance can be limited to object Name if
	needed.
	Note: 	does not support keyword-arguments like -> sort(cmp=myfn)
			or sequence unpacking.	
	"""
	@accepts(Expression, Expression, Name, Expressions)
	def __init__(self, instance, function_name, parameters):
		self.obj = instance
		self.fn_name = function_name
		self.params = parameters

class Attribute(Expression):
	""" 
	Access object's data attribute such as:
	foo.binky
	bar(foo).winky
	"""
	@accepts(Expression, Expression, Name)
	def __init__(self, instance, attr):
		self.obj = instance
		self.attr = attr

class NilExpression(Expression):
	""" Nil expression """
	@accepts(Expression)
	def __init__(self):
		pass

class BoolOp(Expression):
	""" Boolean Operation """
	@accepts(Expression, BooleanOperator, Expressions)
	def __init__(self, operator, expressions):
		self.op = operator
		self.exprs = expressions

class BinOp(Expression):
	""" Binary Operation """
	@accepts(Expression, Expression, BinaryOperator, Expression)
	def __init__(self, left_expr, operator, right_expr):
		self.left = left_expr
		self.op = operator
		self.right = right_expr

class UnaryOp(Expression):
	""" Unary Operation """
	@accepts(Expression, UnaryOperator, Expression)
	def __init__(self, operator, right_expr):
		self.op = operator
		self.right = right_expr	

class CompareOp(Expression):
	""" Compare Operation """
	@accepts(Expression, Expression, CompareOperator, Expression)
	def __init__(self, left_expr, operator, right_expr):
		self.left = left_expr
		self.op = operator
		self.right = right_expr

class IntLiteral(Constant):
	""" Integer Literal """
	@accepts(Expression, int)
	def __init__(self, value):
		self.value = value

class FloatLiteral(Constant):
	""" Float Literal """
	@accepts(Expression, float)
	def __init__(self, value):
		self.value = value

class StringLiteral(Constant):
	""" String Literal """
	@accepts(Expression, str)
	def __init__(self, value):
		self.value = value

class BooleanLiteral(Constant):
	""" Boolean literal, True or False """
	@accepts(Expression, bool)
	def __init__(self, value):
		self.value = value

# Boolean Operators
class And(BooleanOperator):
	def __init__(self):
		pass
class Or(BooleanOperator):
	def __init__(self):
		pass

# Binary Operators
class Add(BinaryOperator):
	def __init__(self):
		pass
class Sub(BinaryOperator):
	def __init__(self):
		pass
class Mult(BinaryOperator):
	def __init__(self):
		pass
class Div(BinaryOperator):
	def __init__(self):
		pass
class Mod(BinaryOperator):
	def __init__(self):
		pass

# Unary Operators
class UPlus(UnaryOperator):
	def __init__(self):
		pass
class UMinus(UnaryOperator):
	def __init__(self):
		pass
class Not(UnaryOperator):
	def __init__(self):
		pass

# Compare Operators
class Eq(CompareOperator):
	def __init__(self):
		pass
class Neq(CompareOperator):
	def __init__(self):
		pass
class Lt(CompareOperator):
	def __init__(self):
		pass
class Gt(CompareOperator):
	def __init__(self):
		pass
class Leq(CompareOperator):
	def __init__(self):
		pass
class Geq(CompareOperator):
	def __init__(self):
		pass
class Is(CompareOperator):
	def __init__(self):
		pass
class IsNot(CompareOperator):
	def __init__(self):
		pass
class In(CompareOperator):
	def __init__(self):
		pass
class NotIn(CompareOperator):
	def __init__(self):
		pass


'''
TODO: 
	--Short-hand if-else: "a if x < 5 else b"
	--Attribute access: "obj.attr"
	--List, set, dict comprehensions
	--List, set, dict access, lookup etc.

'''

