"""
Definitions of AST operator class hierarcy.
Imported into pseudoast. This module makes
pseudoast less cluttered.
"""

# Base Operator class. Do not instantiate
class Operator(AST):
	pass

# Base class for 'And' and 'Or' operators
class BooleanOperator(Operator):
	pass

# Base class for Add, Sub, Mult, Div and Mod
class BinaryOperator(Operator):
	pass

# Base class for UPlus, UMinus, Not
class UnaryOperator(Operator):
	pass

# Base class for all comparators
class CompareOperator(Operator):
	pass

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
class isNot(CompareOperator):
	def __init__(self):
		pass
class In(CompareOperator):
	def __init__(self):
		pass
class NotIn(CompareOperator):
	def __init__(self):
		pass