from django.shortcuts import render

from backend.pseudo_parser import PseudoParser
from backend.lollify import *
from backend.python_codegen import *
import backend.train_examples as train
import argparse

def index(request):
	context = {}
	return render(request, 'translator/index.html', context)

def get_code(request):
	pseudocode = request.POST['pseudocode']
	train_trees = train.train_trees_all()
	test_stmts = pseudocode.split('\n')
	parser = PseudoParser.train(trees=train_trees)

	parse_tree = parser.parse(test_stmts)
	ast = lollify_root(parse_tree)
	code = emit_pycode(ast, None)

	return render(request, 'translator/index.html', {
		'code': code,
		'pseudocode': pseudocode,
	})