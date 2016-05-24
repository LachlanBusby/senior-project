#!/usr/bin/python

from constituent import Constituent


class Tree:
    """Represent linguistic trees, with each node consisting of a label and a list of children.
    Original Java Code by Dan Klein."""

    # The leaf constructor
    def __init__(self, label, indent, line, children=[], parent=None):
        self.label = label
        self.indent = indent
        self.line = line
        self.children = children
        self.parent = parent

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
        return self.children is None # is children ever None??

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

    def getLine(self):
        """ 
        if the node is a STMT node, returns the yield 
        minus the yield for any body statements 
        """
        if not self.isStmt():
            return None 
        return self.getYield(True)


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
        return Tree.fromStringHelper(lines)

    @staticmethod
    def fromStringHelper(lines, last_parent=None):
        root = None
        for l in lines:
            label, line, indent = l.strip().translate(None, '()').split(',')
            line = int(line)
            indent = int(indent)
            if last_parent is None:
                # this is the root node
                root = Tree(label, indent, line, [], None)
                last_parent = root
            elif indent > last_parent.indent:
                # the last parent must be this child's parent
                new_tree = Tree(label, indent, line, [], last_parent)
                last_parent.children.append(new_tree)
                if last_parent == root:
                    last_parent = new_tree
            elif indent == last_parent.indent:
                # they have the same parent
                last_parent = last_parent.parent
                new_tree = Tree(label, indent, line, [], last_parent)
                last_parent.children.append(new_tree)
                if last_parent == root:
                    last_parent = new_tree
            elif indent < last_parent.indent:
                # traverse up the parents tree until you find an indent less than our current indent
                while indent <= last_parent.parent:
                    last_parent = last_parent.parent
                new_tree = Tree(label, indent, line, [], last_parent)
                last_parent.children.append(new_tree)
                if last_parent == root:
                    last_parent = new_tree

        return root

    # Returns a string representation of this tree using bracket notation.
    def toString(self):
        string = '\t' * self.indent
        if not self.isLeaf():
            string += '('
        if self.getLabel() is not None:
            string += self.getLabel() + ',' + str(self.line) + ',' + str(self.indent)
        if not self.isLeaf():
            
            print self.label + ": " + str(self.children) + "\n"
            for child in self.children:
                string += '\n' + child.toString()
            string += ')'
        return string

    def deepCopy(self, tree=None):
        if tree is None: return self.deepCopy(self)

        childrenCopies = []
        for child in self.children:
            childrenCopies.append(self.deepCopy(child))
        return Tree(tree.getLabel(), childrenCopies)

    def productions(self):
        prods = []
        if self.isProgram():
            prods.extend(self.children[0].productions())
        elif self.isStmtList():
            for child in self.children:
                prods.extend(child.productions())
        elif self.isStmt():
            prods = self.children[0].productions()
        elif not self.isLeaf():
            rhs = []
            for child in children:
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
        for child in children:
            if child.isStmtList():
                continue
            prods.extend(child.productions())
            rhs_elem = child.label if child.isLeaf() else nltk.grammar.Nonterminal(child.label)
            rhs.append(rhs_elem)
        prods.append(nltk.grammar.Production(nltk.grammar.Nonterminal(self.label), rhs))
        return prods
