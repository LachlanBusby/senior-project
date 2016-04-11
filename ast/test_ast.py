from pseudoast import *

"""
Creates an AST for the following python program:
def myfn1(arg1, arg2, arg3):
	return 1

def myfn2():
	return 5

def main():
	x = 0
	while 0 <= x < 15:
		y = myfn1(x + -5.0, "mystr", not True)
		x += y
		if y == 1:
			continue
		elif y == 2:
			break
		else:
			myfn2(x)

		x += 1
"""


if __name__== "__main__":
	x_token = Name("x")
	y_token = Name("y")
	int0 = IntLiteral(0)
	int1 = IntLiteral(1)
	int2 = IntLiteral(2)
	int5 = IntLiteral(5)
	int15 = IntLiteral(15)
	float5 = FloatLiteral(5.0)
	mystr = StringLiteral("mystr")
	arg1 = Argument(Name("arg1"))
	arg2 = Argument(Name("arg2"))
	arg3 = Argument(Name("arg3"))
	myfn1_token = Name("myfn1")
	myfn2_token = Name("myfn2")
	main_token = Name("main")
	true_token = BooleanLiteral(True)
	myfn1 = FunctionDef(myfn1_token, 
						Arguments([
							arg1, arg2, arg3
						]), 
						Statements([
							Return(int1)
						]))
	myfn2 =  FunctionDef(myfn1_token, 
						Arguments([]), 
						Statements([
							Return(int5)
						]))
	assign_to_y = Assign(
					y_token, 
					Call(
						myfn1_token, 
						Expressions([
							Add(
								x_token, 
								UMinus(float5)),
							mystr,
							Not(true_token)
					])))
	augAssign_y_to_x = AugAssign(
							x_token, 
							Plus(), 
							y_token)
	augAssign_1_to_x = AugAssign(
							x_token, 
							Plus(), 
							int1)
	else_stmts = Statements([
						ExprStmt(
							Call(
								myfn2_token, 
								Expressions([
									x_token
								])
							))
						])
	elif_stmts = Statements([
							If(
								Compare(
									y_token, 
									CompareOperators([
										Eq()
									]), 
									Expressions([
										int2
									])),
								Statements([
									Break()
								]),
								else_stmts
							)])
	if_stmts = If(
				Compare(
					y_token, 
					CompareOperators([
						Eq()
					]), 
					Expressions([
						int1
					])),
				Statements([
					Continue()
				]), 
				elif_stmts)

	while_loop = While(
					Compare(int0, 
							CompareOperators([
								Leq(), Lt()
							]), 
							Expressions([
								x_token, int15
							])),
					Statements([
						assign_to_y,
						augAssign_y_to_x,
						if_stmts,
						augAssign_1_to_x
					]))
	main_def = FunctionDef(
					main_token,
					Arguments([]),
					Statements([
						Assign(
							x_token,
							int0),
						while_loop])
					)

	program_node = Program(Statements([myfn1, myfn2, main_def]))
	serialized = serialize(program_node)
	deserialized = deserialize(serialized)
	print "Program node using repr:\n%s" %repr(program_node)





