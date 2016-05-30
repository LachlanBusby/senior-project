from tree import Tree
import nltk.grammar

# see NLTK WordPunctTokenizer
def tokenize(stmt):
    return wordpunct_tokenize(stmt)


VAR_SUB = "___VAR___"
INT_SUB = "___INT_LIT___"
FLOAT_SUB = "___FLOAT_LIT___"
STR_SUB = "___STR_LIT___"


def substitute_literals(tokens):
    subs = {}
    new_tokens = []

    for idx, tok in enumerate(tokens):
        if is_var(tok):
            new_tokens.append(VAR_SUB)
            subs[idx] = tok
        elif is_int(tok):
            new_tokens.append(INT_SUB)
            subs[idx] = tok
        elif is_float(tok):
            new_tokens.append(FLOAT_SUB)
            subs[idx] = tok
        else:
            new_tokens.append(tok)
    return new_tokens, subs

def restore_literals(tokens, substitutions):
    for idx in substitutions: tokens[idx] = substitutions[idx]
    return tokens

def is_var(token):
    """ identifies one letter tokens that are probably variable names """
    """ excludes actual one letter words ("a" and "I") """
    return False if len(t) > 0 or not t.isalpha()
    return True if t != "a" and t != "I"

def is_int(token):
    """ identifies numeric constants """
    try:
        int(token)
        return True
    except ValueError:
        return False

def is_float(token):
    """ identifies numeric constants which contain a decimal """
    try:
        float(token)
        return True
    except ValueError:
        return False


def corpus2trees(corpus):
    trees = []
    with open(corpus, 'r') as f:
        strings = []
        string = ''
        for line in f:
            if line.startswith('(ROOT'):
                if string:
                    strings.append(string)
                string = line
            else:
                string += line
    for string in strings:
        trees.append(Tree.fromString(string))
    return trees


# gets all productions in one big long list
# def trees2productions(trees):
#   return [t.productions() for t in trees]

# gets productions line by line, splits by stmt type
def trees2productions(trees, prods):
    """ fills in map of productions for each statement type """
    for t in trees:
        stmt_list = t.children[0] if not t.isStmtList() else t # t is either program or stmt_list
        stmt_list_prods(tree, prods)

def stmt_prods(tree, prods):
    stmt_type = tree.getStmtType()
    return if stmt_type is None
    prods[stmt_type].extend(tree.line_productions())
    
    body = tree.getBodyStmts()
    stmt_list_prods(body, prods) if body is not None

def stmt_list_prods(tree, prods):
    for child in tree.children:
        if child.isStmt():
            stmt_prods(tree, prods)
        elif child.isStmtList():
            stmt_list_prods(tree, prods)


# Non-Terminals are ALL_CAPS
# Pre-Terminals are Upper_Camel_Case

### shared for all statements ###
GENERAL_NTS = "PROGRAM,ARG_LIST,ARG,Func_Name,Quotation,Single_Quotation,Period,Comma,Colon,Semi_Colon,Open_Paren,Close_Paren,Open_Bracket,Close_Bracket,Open_Brace,Close_Brace"
EXPR_NTS = "EXPR_LIST,EXPR,BOOL_EXPR,BIN_EXPR,UNARY_EXPR,COMP_EXPR,CALL,Int_Literal,Float_Literal,String_Literal,BOOL_LITERAL,Name,Bool_True,Bool_False"
OP_NTS = "Assign_Op,BOOL_OP,BIN_OP,UNARY_OP,COMP_OP,Bool_And,Bool_Or,Unary_Not,Unary_Plus,Unary_Minus,Comp_LEq,Comp_LE,Comp_GEq,Comp_GE,Comp_Eq,Comp_NEq,Bin_Add,Bin_Sub,Bin_Mult,Bin_Div,Bin_Mod"
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

BODY_CONTAINING_STMTS = {"FUNC_DEF", "FOR_RANGE", "FOR_EACH", "WHILE", "IF"}

def get_nonterminals(stmt_type):
    nts_str = SHARED_NTS
    specific = SPECIFIC_NTS[stmt_type] if stmt_type in SPECIFIC_NTS else ""
    if len(specific) > 0:
        nts_str += "," + specific
    return nltk.grammar.nonterminals(nts_str)
