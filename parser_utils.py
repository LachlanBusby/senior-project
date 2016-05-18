from tree import Tree
from nltk.tokenize import wordpunct_tokenize


# see NLTK WordPunctTokenizer
def tokenize_stmt(stmt):
    return wordpunct_tokenize(stmt)


VAR_SUB = "___VAR___"
INT_SUB = "___INT_LIT___"
FLOAT_SUB = "___FLOAT_LIT___"
STR_SUB = "___STR_LIT___"


def sub_tokens(tokens):
    subs = []
    new_tokens = []
    for t in tokens:
        if is_var(t):
            new_tokens.append(VAR_SUB)
            subs.append(t)
        elif is_int(t):
            new_tokens.append(INT_SUB)
            subs.append(t)
        elif is_float(t):
            new_tokens.append(FLOAT_SUB)
            subs.append(t)
    return new_tokens, subs


def is_var(token):
    if len(token) > 0 or not token.isalpha():
        return False
    if token != "a" and token != "I":
        return True


def is_int(token):
    try:
        int(token)
        return True
    except ValueError:
        return False


def is_float(token):
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
