from parser_utils import *
from tree import Tree
from stmt_classifier import StmtClassifier
from stmt_parser import StmtParser
import nltk

class PseudoParser():
    def __init__(self, productions, stmts, stmt_types):
        self.parsers = {}
        for stmt_type in productions:
            if len(productions[stmt_type]) == 0:
                continue
            pcfg = nltk.grammar.induce_pcfg(nltk.grammar.Nonterminal(stmt_type), productions[stmt_type])
            self.parsers[stmt_type] = StmtParser(pcfg)

        self.clf = StmtClassifier()
        self.clf.train(stmts, stmt_types)

    @classmethod
    def train(cls, filename=None, trees=None):
        if filename is None and trees is None:
            return None

        if filename is not None and trees is None:
            with open(filename, 'r') as f:
                corpus = f.read()
                print corpus
            trees = corpus2trees(corpus)

        trees, subs = preprocess_trees(trees)
        productions = trees2productions(trees)
        stmts, types = trees2stmts(trees)

        # print_productions(productions, trees)
        return cls(productions, stmts, types)

    @staticmethod
    def _tokenize(stmt):
        tokens = tokenize(stmt)
        subs = {}
        tokens, subs = sub_literals(tokens, subs)
        tokens, subs = guess_func_names(tokens, subs)
        return tokens

    @staticmethod
    def _setStmtYield(tree, stmt):
        tokens = tokenize(stmt)
        tree.setWords(tokens)
        return tree

    def parse(self, stmts):
        """ takes in a list of lines/statements and returns full parse tree """
        tree = Tree("PROGRAM", children=[])
        parentNode = Tree("STMT_LIST",indent=0,parent=tree)
        tree.children.append(parentNode)
        
        for line, stmt in enumerate(stmts):
            indent = len(stmt) - len(stmt.lstrip('\t'))
            while True:
                if parentNode.isStmtList() and indent == parentNode.getIndent():
                    break
                if parentNode.isStmt() and indent == parentNode.getIndent() + 1:
                    break
                parentNode = parentNode.getParent()

            if parentNode.isStmt():
                parentNode = parentNode.children[0]
                list_tree = Tree("STMT_LIST", indent, parent = parentNode)
                parentNode.children.append(list_tree)
                parentNode = list_tree

            if len(parentNode.children) == 1:
                list_tree = Tree("STMT_LIST", indent, parent = parentNode)
                parentNode.children.append(list_tree)
                parentNode = list_tree

            tokens = self._tokenize(stmt)
            stmt_types = self.clf.classify(" ".join(tokens))

            parse_tree = None
            for t in stmt_types:
                parse_tree = self.parsers[t].parse(tokens, stmt)
                if parse_tree is not None: break
            if parse_tree is None:
                raise ValueError("Parsers were unable to parse this line." %tokens)

            stmt_tree = Tree("STMT", indent, line, parent=parentNode)
            parse_tree.parent = stmt_tree
            stmt_tree.children.append(parse_tree)
            if not parse_tree.isError():
                stmt_tree = self._setStmtYield(stmt_tree, stmt)
            stmt_tree.parent = parentNode
            parentNode.children.append(stmt_tree)
            parentNode = stmt_tree
        return tree
