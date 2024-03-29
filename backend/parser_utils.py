import re
from tree import Tree
import nltk.grammar
from nltk.tokenize import wordpunct_tokenize

STMT_TYPES = ["FUNC_DEF", "RETURN", "ASSIGN", "AUG_ASSIGN", "FOR_RANGE", "FOR_EACH", "WHILE", "IF", "BREAK", "CONTINUE", "EXPR_STMT"]
ROOT_TYPE = "PROGRAM"

def convert_nltk_tree(t):
    if not isinstance(t, nltk.Tree):
        return Tree(t)
    converted = Tree(t.label())
    for c in t:
        child = convert_nltk_tree(c)
        child.parent = converted
        converted.children.append(child)
    return converted

# see NLTK WordPunctTokenizer

def tokenize(stmt):
    tokens = wordpunct_tokenize(stmt)
    hotfix_tokens = fix_hyphens(tokens)
    return fix_augassign(hotfix_tokens)

def fix_augassign(tokens):
    ret = []
    for token in tokens:
        if len(token) == 2 and token[1] == '=' and token[0] in ['+', '-', '%', '*', '/']:
            ret += [token[0], token[1]]
        else:
            ret.append(token)
    return ret

def fix_hyphens(tokens):
    if len(tokens) < 3:
        return tokens

    new_tokens = [tokens[0]]
    i = 1
    while i < len(tokens):
        tok = tokens[i]
        if i+1 < len(tokens) and tok == '-' and new_tokens[-1].isupper() and tokens[i+1].isupper():
            new_tokens[-1] = new_tokens[-1] + "-" + tokens[i+1]
            i += 2 # skip tokens[i+1]
        else:
            new_tokens.append(tok)
            i += 1
    return new_tokens

VAR_SUB = "___VAR___"
INT_SUB = "___INT_LIT___"
FLOAT_SUB = "___FLOAT_LIT___"
STR_SUB = "___STR_LIT___"
FUNC_NAME_SUB = "___FUNC_NAME___"

def preprocess_trees(trees):
    subs = []
    for t in trees:
        tokens, t_subs = sub_func_names(t)
        tokens, t_subs = sub_literals(tokens, t_subs)
        t.setWords(tokens)
        subs.append(t_subs)
    return trees, subs

def postprocess_trees(trees, substitutions):
    for idx, t in enumerate(trees):
        sub_yield = t.getYield()
        orig_yield = restore_tokens(sub_yield, substitutions[idx])
        t.setWords(orig_yield)
    return trees

def sub_func_names(tree):
    preterms = tree.getPreTerminalYield()
    tokens = []
    subs = {}
    for idx, tok in enumerate(tree.getYield()):
        if preterms[idx] == "Func_Name":
            tokens.append(FUNC_NAME_SUB)
            subs[idx] = tok
        else:
            tokens.append(tok)
    return tokens, subs

def sub_literals(tokens, subs):
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

def guess_func_names(tokens, subs):
    new_tokens = []
    for idx, tok in enumerate(tokens):
        if is_func_name(tok):
            new_tokens.append(FUNC_NAME_SUB)
            subs[idx] = tok
        else:
            new_tokens.append(tok)
    return new_tokens, subs

def restore_tokens(tokens, substitutions):
    for idx in substitutions: tokens[idx] = substitutions[idx]
    return tokens

def is_var(token):
    """ identifies one letter tokens that are probably variable names """
    return len(token) == 1 and token.isalpha()

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

def is_func_name(token):
    if len(token) <= 1: return False
    if is_var(token) or is_int(token) or is_float(token): return False

    if token == "print": return True
    if re.match(r"^[A-Z0-9]+[A-Z0-9-]*$", token) is not None: return True
    return False

# print "ADD-TWO-NUMBERS: " + str(is_func_name("ADD-TWO-NUMBERS"))
# print "for: " + str(is_func_name("for"))
# print "A: " + str(is_func_name("A"))
# print "PRINT: " + str(is_func_name("PRINT"))
# print "print: " + str(is_func_name("print"))
# print "PRINT-TO-NUMBER: " + str(is_func_name("PRINT-TO-NUMBER"))
# print "PRINT-TO-NUMBER2: " + str(is_func_name("PRINT-TO-NUMBER2"))
# print "32: " + str(is_func_name("32"))
# print "___INT_LIT___: " + str(is_func_name(INT_SUB))

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
def trees2productions(trees):
    prods = {stmt_type: [] for stmt_type in STMT_TYPES}
    expr_prods = []

    # fills in map of productions for each statement type
    for t in trees:
        stmt_list = t.children[0] if not t.isStmtList() else t # t is either program or stmt_list
        stmt_list_prods(t, prods, expr_prods)

    #adds all expr productions to the end of each stmt production list
    for stmt_type in STMT_TYPES: prods[stmt_type].extend(expr_prods)
    return prods

def stmt_prods(tree, prods, expr_prods):
    stmt_type = tree.getStmtType()
    if stmt_type is not None:
        stmt_ps, expr_ps = tree.productions()
        prods[stmt_type].extend(stmt_ps)
        expr_prods.extend(expr_ps)
        body = tree.getStmtBody()
        if body is not None:
            stmt_list_prods(body, prods, expr_prods)

def stmt_list_prods(tree, prods, expr_prods):
    for child in tree.children:
        if child.label == "STMT":
            stmt_prods(child, prods, expr_prods)
        elif child.label == "STMT_LIST":
            stmt_list_prods(child, prods, expr_prods)

def print_productions(prods, trees=None):
    if trees is not None and len(trees) == 1:
        print "Tree: "
        print trees[0].toString()
        print "\n\n\n"
    for stmt_type in prods:
        p_list = ", ".join([ p.unicode_repr() for p in prods[stmt_type]])
        print stmt_type + ": [" + p_list + "]"

def trees2stmts(trees):
    stmts = []
    types = []
    for t in trees:
        t_stmts, t_types = t.get_stmt_types()
        stmts.extend(t_stmts)
        types.extend(t_types)
    return stmts, types

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

BODY_CONTAINING_STMTS = ["FUNC_DEF", "FOR_RANGE", "FOR_EACH", "WHILE", "IF"]

def get_nonterminals(stmt_type):
    nts_str = SHARED_NTS
    specific = SPECIFIC_NTS[stmt_type] if stmt_type in SPECIFIC_NTS else ""
    if len(specific) > 0:
        nts_str += "," + specific
    return nltk.grammar.nonterminals(nts_str)

def shouldHaveBody(stmt_type):
    return stmt_type in BODY_CONTAINING_STMTS