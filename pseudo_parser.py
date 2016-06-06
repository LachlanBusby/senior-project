import parser_utils
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
            trees = parser_utils.corpus2trees(corpus)
        trees, subs = parser_utils.preprocess_trees(trees)
        productions = {stmt_type: [] for stmt_type in parser_utils.STMT_TYPES}
        parser_utils.trees2productions(trees, productions)
        # for p in productions:
        #     p_strs = []
        #     for r in productions[p]:
        #        p_strs.append(r.unicode_repr())
        #     print p + " : [" + "; ".join(p_strs) + "]"

        stmts, types = parser_utils.trees2stmts(trees)
        return cls(productions, stmts, types)

    @staticmethod
    def _tokenize(stmt):
        tokens = parser_utils.tokenize(stmt)
        tokens, subs = parser_utils.substitute_literals(tokens)
        return tokens

    @staticmethod
    def _setStmtYield(tree, stmt):
        tokens = parser_utils.tokenize(stmt)
        tree.setWords(tokens)
        return tree

    def parse(self, stmts):
        """ takes in a list of lines/statements and returns full parse tree """
        numStatements = len(stmts)
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
                parse_tree = self.parsers[t].parse(tokens)
                if parse_tree is not None: break
            if parse_tree is None:
                raise ValueError("Something fucked up. None of the parsers recognize this shit. (%s)" %tokens)

            stmt_tree = Tree("STMT", indent, line, parent=parentNode)
            parse_tree.parent = stmt_tree
            stmt_tree.children.append(parse_tree)
            stmt_tree = self._setStmtYield(stmt_tree, stmt)
            stmt_tree.parent = parentNode
            parentNode.children.append(stmt_tree)
            parentNode = stmt_tree
        return tree
