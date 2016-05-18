# Non-Terminals are ALL_CAPS
# Pre-Terminals are Upper_Camel_Case

### shared for all statements ###
GENERAL_NTS = "PROGRAM,ARG_LIST,ARG,Func_Name,Quotation,Single_Quotation,Period,Comma,Colon,Semi_Colon,Open_Paren,Close_Paren,Open_Bracket,Close_Bracket,Open_Brace,Close_Brace"
EXPR_NTS = "EXPR_LIST,EXPR,BOOL_EXPR,BIN_EXPR,UNARY_EXPR,COMP_EXPR,CALL,Int_Literal,Float_Literal,String_Literal,Bool_Literal,Name"
OP_NTS = "Assign_Op,Bool_Op,Bin_Op,Unary_Op,Comp_Op"
STMT_NTS = "STMT_LIST,STMT,FUNC_DEF,RETURN,ASSIGN,AUG_ASSIGN,FOR_RANGE,FOREACH,WHILE,IF,BREAK,CONTINUE,EXPR_STMT"

SHARED_NTS = GENERAL_NTS + "," + EXPR_NTS + "," + OP_NTS + "," + STMT_NTS

### specific to statement types ###
FUNC_DEF_NTS = ""
RETURN_NTS = "Return_Keyword"
ASSIGN_NTS = ""
AUG_ASSIGN_NTS = ""
FOR_RANGE_NTS = "FOR_START,FOR_CONDITION,FOR_END,FOR_OPERATION,For_Range_Keyword,For_Op_Keyword,For_LEQ,For_GEQ,For_LE,For_GE"
FOR_EACH_NTS = "" # TODO
WHILE_NTS = "While_Keyword"
IF_NTS = "If_Keyword,ELSE_IF,ELSE,Else_Keyword"
BREAK_NTS = "Break_Keyword"
CONTINUE_NTS = "Continue_Keyword"
EXPR_STMT_NTS = "" # DOUBLE CHECK


SPECIFIC_NTS = {"FUNC_DEF" : FUNC_DEF_NTS,
				"RETURN" : RETURN_NTS,
				"ASSIGN" : ASSIGN_NTS,
				"AUG_ASSIGN" : AUG_ASSIGN_NTS,
				"FOR_RANGE" : FOR_RANGE_NTS,
				"FOR_EACH" : FOR_EACH_NTS,
				"WHILE" : WHILE_NTS,
				"IF" : IF_NTS,
				"BREAK" : BREAK_NTS,
				"CONTINUE" : CONTINUE_NTS,
				"EXPR_STMT" : EXPR_STMT_NTS}


def get_nonterminals(stmt_type):
	specific = SPECIFIC_NTS[stmt_type] if stmt_type in SPECIFIC_NTS else ""
	if len(specific) > 0:
		return SHARED_NTS + "," + specific 
	else:
		return SHARED_NTS


