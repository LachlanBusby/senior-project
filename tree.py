#!/usr/bin/python
import logging
import nltk

from constituent import Constituent


class Tree:
    """Represent linguistic trees, with each node consisting of a label and a list of children.
    Original Java Code by Dan Klein."""

    # The leaf constructor
    def __init__(self, label, indent=-1, line=-1, children=None, parent=None):
        self.label = label
        self.indent = indent
        self.line = line
        self.children = children if children is not None else []
        self.parent = parent

    def __repr__(self):
        return self.toString()

    def getChildren(self):
        return self.children

    def setChildren(self, children):
        self.children = children

    def getLabel(self):
        return self.label

    def setLabel(self, label):
        self.label = label

    def getParent(self):
        return self.parent

    def setParent(self, parent):
        self.parent = parent

    def getIndent(self):
        return self.indent

    def setIndent(self, indent):
        self.indent = indent

    def getLine(self):
        return self.line

    def setLine(self, line):
        self.line = line

    # Returns true at the word(leaf) level of a tree
    def isLeaf(self):
        if self.label == "STMT" or self.label == "STMT_LIST":
            return False
        return len(self.children) == 0 # is children ever None??

    # Returns true level of non-terminals which are directly above
    # single words(leafs)
    def isPreTerminal(self):
        return len(self.children) == 1 and self.children[0].isLeaf()

    def isPhrasal(self):
        return not (self.isLeaf() or self.isPreTerminal())

    def isStmt(self):
        if self.label == "STMT":
            if len(self.children) != 1:
                logging.error("STMT nodes should only have 1 child.") 
            return True
        return False


    def isStmtList(self):
        if self.label == "STMT_LIST":
            if len(self.children) > 2:
                logging.error("STMT_LIST nodes should have at most 2 children.")
            return True
        return False

    def isProgram(self):
        if self.label == "PROGRAM":
            if len(self.children) != 1:
                logging.error("PROGRAM nodes should have 1 STMT_LIST child.")
            return True
        return False

    def getStmtType(self):
        """ if node is a statement node, returns the label for the child node """
        if not self.isStmt():
            return None
        else:
            return self.children[0].label

    # returns true if children contains STMT_LIST node
    def hasBodyStmts(self):
        """ returns true if children contains STMT_LIST node """
        for child in self.children:
            if child.isStmtList():
                return True 
        return False

    def getBodyStmts(self):
        """ returns STMT_LIST node in children or None if there isn't one """
        for child in self.children:
            if child.isStmtList():
                return child 
        return None

    def getStmtBody(self):
        if self.isStmt() and len(self.children) == 1:
            stmt_child = self.children[0]
            return stmt_child.getChild("STMT_LIST")
        return None

    def getChild(self, label, index=0):
        """
        returns first child after specified index with the desired label
        returns None if no child is found with that label
        """
        for c in self.children[index:]:
            if c.label == label:
                return c
        return None

    def getLine(self):
        """ 
        if the node is a STMT node, returns the yield 
        minus the yield for any body statements 
        """
        if not self.isStmt():
            return None 
        return " ".join(self.getYield(True))


    # Returns a list of words at the leafs of this tree gotten by
    # traversing from left to right
    def getYield(self, line_only=False):
        yield_list = []
        self.appendYield(self, yield_list)
        return yield_list

    def appendYield(self, tree, yield_list,line_only=False):
        if tree.isLeaf():
            yield_list.append(tree.getLabel())
            return
        for child in tree.getChildren():
            if line_only and child.isStmtList():
                continue 
            self.appendYield(child, yield_list)

    # Returns a list of the preterminals gotten by traversing from left
    # to right. This is effectively a POS tagging for the words that
    # tree represents.
    def getPreTerminalYield(self):
        yield_list = []
        self.appendPreTerminalYield(self, yield_list)
        return yield_list

    def appendPreTerminalYield(self, tree, yield_list):
        if tree.isPreTerminal():
            yield_list.append(tree.getLabel())
            return
        for child in tree.getChildren():
            self.appendPreTerminalYield(child, yield_list)

    # Returns a list of the node values gotten by traversing in this
    # order: root, left subtree, right subtree
    def getPreOrderTraversal(self):
        traversal = []
        self.traversalHelper(self, traversal, True)
        return traversal

    # Returns a list of the node values gotten by traversing in this
    # order: left subtree, right subtree, root
    def getPostOrderTraversal(self):
        traversal = []
        self.traversalHelper(self, traversal, False)
        return traversal

    def traversalHelper(self, tree, traversal, preOrder):
        if preOrder:
            traversal.append(tree)
        for child in tree.getChildren():
            self.traversalHelper(child, traversal, preOrder)
        if not preOrder:
            traversal.append(tree)

    # Set the words at the leaves of a tree to the words from the list
    def setWords(self, words):
        self.setWordsHelper(words, 0)

    def setWordsHelper(self, words, wordNum):
        if self.isLeaf():
            self.label = words[wordNum]
            return wordNum + 1
        else:
            for child in self.children:
                wordNum = child.setWordsHelper(words, wordNum)
            return wordNum

    def toSubTreeList(self):
        return self.getPreOrderTraversal()

    # Creates a list of all constituents in this tree. A constituent
    # is just a non-terminal label and that non-terminal covers in the tree.
    def toConstituentList(self):
        constituent_list = []
        self.toConstituentListCollectionHelper(self, 0, constituent_list)
        return constituent_list

    def toConstituentListCollectionHelper(self, tree, start, constituents):
        if tree.isLeaf() or tree.isPreTerminal():
            return 1
        span = 0
        for child in tree.getChildren():
            span += self.toConstituentListCollectionHelper(child, start + span, constituents)
        constituents.append(Constituent(tree.getLabel(), start, start + span))
        return span

    @staticmethod
    def fromString(string):
        lines = string.split('\n')
        built_trees = []
        root = None
        for l in lines:
            str_indent = l.count('\t')
            l = l.strip().translate(None, ':')
            line = -1
            indent = -1
            lst = l.split(' ')
            n_str = []
            for s in lst:
                if not (len(s) == s.count('(') or len(s) == s.count(')')):
                    n_str.append(s)
            l = ''.join(n_str)
            if l:
                if ',' in l:
                    label, line, indent = l.split(',')
                else:
                    label = l
                line = int(line) if line != 'None' else None
                indent = int(indent) if indent != 'None' else None
                new_tree = Tree(label, line, indent, [], None)
                if label == 'STMT_LIST' and len(built_trees) == 1:
                    # this has to be attached to the root node
                    root.children.append(new_tree)
                    new_tree.parent = root
                elif label == 'STMT' or label == 'STMT_LIST':
                    for i in reversed(xrange(len(built_trees))):
                        t, ind = built_trees[i]
                        if t.isStmtList() and ind == str_indent-1:
                            new_tree.parent = t
                            t.children.append(new_tree)
                            break
                else:
                    if len(built_trees) == 0:
                        # this is the root
                        root = Tree(label, line, indent, [], None)
                    else:
                        for i in reversed(xrange(len(built_trees))):
                            # iterate until we find a suitable parent
                            t, ind = built_trees[i]
                            if ind == str_indent-1:
                                new_tree.parent = t
                                t.children.append(new_tree)
                                break
                built_trees.append((new_tree, str_indent))
        return root

### TODO ###
    # @staticmethod
    # def fromStringV2(string):
    #     lines = string.split('\n')
    #     built_trees = []
    #     root = None
    #     for l in lines:
    #         stripped = l.lstrip('\t')
    #         indent = len(l) - stripped
    #         stripped = l.lstrip('(')

    # Returns a string representation of this tree using bracket notation.
    def toString(self):
        return self.toStringHelper(0)

    def toStringHelper(self, nindent):
        string = '' + "".join([' ']*(4*nindent))
        
        if self.isLeaf():
            string += "(\'" + self.label + "\')"
        else:
            string += "(" + self.label
            if self.label == "STMT_LIST":
                string += ',' + str(self.indent) + ':'
            elif self.label == "STMT":
                string += ',' + str(self.indent) + ',' + str(self.line) + ':'
        
            if len(self.children) > 0:
                for child in self.children:
                    string += '\n' + child.toStringHelper(nindent+1)
            string += ')'

        return string

    def deepCopy(self, tree=None):
        if tree is None: return self.deepCopy(self)

        childrenCopies = []
        for child in self.children:
            childrenCopies.append(self.deepCopy(child))
        return Tree(tree.getLabel(), childrenCopies)

    def stmt_productions(self):
        if not self.isStmt():
            return []

        prods = []
        head = self.children[0]

        rhs = []
        for child in head.children:
            if child.isStmtList():
                continue
            if child.isLeaf():
                rhs.append(child.label)
            else:
                rhs.append(nltk.grammar.Nonterminal(child.label))
            prods.extend(child.productions_v2())

        lhs = nltk.grammar.Nonterminal(head.label)
        prods.append(nltk.grammar.Production(lhs, rhs))
        return prods

    def productions_v2(self):
        prods = []
        if self.isLeaf():
            return prods

        rhs = []
        for child in self.children:
            if child.isLeaf():
                rhs.append(child.label)
            else:
                rhs.append(nltk.grammar.Nonterminal(child.label))
            prods.extend(child.productions_v2())

        if not (self.isProgram() or self.isStmt() or self.isStmtList()):
            lhs = nltk.grammar.Nonterminal(self.label)
            prods.append(nltk.grammar.Production(lhs, rhs))
        return prods

    def productions(self):
        prods = []
        if self.label == "PROGRAM":
            prods.extend(self.children[0].productions())
        elif self.label == "STMT_LIST":
            for child in self.children:
                prods.extend(child.productions())
        elif self.label == "STMT":
            prods = self.children[0].productions()
        elif len(self.children) > 0:
            rhs = []
            for child in self.children:
                prods.extend(child.productions())
                rhs_elem = child.label if child.isLeaf() else nltk.grammar.Nonterminal(child.label)
                rhs.append(rhs_elem)
            prods.append(nltk.grammar.Production(nltk.grammar.Nonterminal(self.label), rhs))
        return prods


    def line_productions(self):
        if not self.isStmt():
            return None
        stmt_head = self.children[0]
        
        rhs = []
        prods = []
        for child in stmt_head.children:
            if child.isStmtList():
                continue
            prods.extend(child.productions())
            rhs_elem = child.label if child.isLeaf() else nltk.grammar.Nonterminal(child.label)
            rhs.append(rhs_elem)
        prods.append(nltk.grammar.Production(nltk.grammar.Nonterminal(stmt_head.label), rhs))
        return prods

    def get_stmt_types(self):
        stmts = []
        types = []

        if self.isStmt():
            stmts.append(self.getLine())
            types.append(self.getStmtType())

        for child in self.children:
            c_stmts, c_types = child.get_stmt_types()
            stmts.extend(c_stmts)
            types.extend(c_types)
        return stmts, types



# used to test from/toString
# s = "( PROGRAM \n\t( STMT_LIST ,None,0:\n\t\t( STMT ,1,0:\n\t\t\t( FUNC_DEF \n\t\t\t\t( Func_Name \n\t\t\t\t\t( 'EXAMPLE-METHOD' )\n\t\t\t\t( Open_Paren \n\t\t\t\t\t( '(' )\n\t\t\t\t( ARG_LIST \n\t\t\t\t\t( ARG \n\t\t\t\t\t\t( EXPR \n\t\t\t\t\t\t\t( Name \n\t\t\t\t\t\t\t\t( 'x' ))))\n\t\t\t\t( Close_Paren \n\t\t\t\t\t( ')' )\n\t\t( STMT_LIST ,None,1:\n\t\t\t( STMT ,2,1:\n\t\t\t\t( IF \n\t\t\t\t\t( If_Keyword \n\t\t\t\t\t\t( 'If' )\n\t\t\t\t\t( EXPR\n\t\t\t\t\t\t( COMP_EXPR\n\t\t\t\t\t\t\t( EXPR\n\t\t\t\t\t\t\t\t( Name\n\t\t\t\t\t\t\t\t\t( 'x'))\n\t\t\t\t\t\t\t( COMP_OP\n\t\t\t\t\t\t\t\t( Comp_LE\n\t\t\t\t\t\t\t\t\t( '<'))\n\t\t\t\t\t\t\t( EXPR\n\t\t\t\t\t\t\t\t( Int_Literal\n\n\t\t\t\t\t\t\t\t\t( '10'))))\n\t\t\t( STMT_LIST ,None,2:\n\t\t\t\t( STMT ,3,2:\n\t\t\t\t\t( EXPR_STMT\n\t\t\t\t\t\t( CALL\n\t\t\t\t\t\t\t( Func_Name\n\t\t\t\t\t\t\t\t( 'print'\n\t\t\t\t\t\t\t( ARG_LIST\n\t\t\t\t\t\t\t\t( ARG\n\t\t\t\t\t\t\t\t\t( EXPR\n\t\t\t\t\t\t\t\t\t\t( Name\n\t\t\t\t\t\t\t\t\t\t\t( 'x' ))))))))))))))))))))))))))"

# print s
# t = Tree.fromString(s)
# print
# print t.toString()
