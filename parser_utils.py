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
	return False if len(t) > 0 or not t.isalpha()
	return True if t != "a" and t != "I"

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

