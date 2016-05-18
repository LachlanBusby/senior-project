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

    # Returns true at the word(leaf) level of a tree
    def is_leaf(self):
        return self.children is None

    # Returns true level of non-terminals which are directly above
    # single words(leafs)
    def is_pre_terminal(self):
        return len(self.children) == 1 and self.children[0].isLeaf()

    def is_phrasal(self):
        return not (self.is_leaf() or self.is_pre_terminal())

    # Returns a list of words at the leafs of this tree gotten by
    # traversing from left to right
    def get_yield(self):
        yield_list = []
        self.append_yield(self, yield_list)
        return yield_list

    def append_yield(self, tree, yield_list):
        if tree.is_leaf():
            yield_list.append(tree.label)
            return
        for child in tree.children:
            self.append_yield(child, yield_list)

    # Returns a list of the preterminals gotten by traversing from left
    # to right. This is effectively a POS tagging for the words that
    # tree represents.
    def get_pre_terminal_yield(self):
        yield_list = []
        self.append_pre_terminal_yield(self, yield_list)
        return yield_list

    def append_pre_terminal_yield(self, tree, yield_list):
        if tree.is_pre_terminal():
            yield_list.append(tree.label)
            return
        for child in tree.children:
            self.append_pre_terminal_yield(child, yield_list)

    # Returns a list of the node values gotten by traversing in this
    # order: root, left subtree, right subtree
    def get_pre_order_traversal(self):
        traversal = []
        self.traversal_helper(self, traversal, True)
        return traversal

    # Returns a list of the node values gotten by traversing in this
    # order: left subtree, right subtree, root
    def get_post_order_traversal(self):
        traversal = []
        self.traversal_helper(self, traversal, False)
        return traversal

    def traversal_helper(self, tree, traversal, pre_order):
        if pre_order:
            traversal.append(tree)
        for child in tree.children:
            self.traversal_helper(child, traversal, pre_order)
        if not pre_order:
            traversal.append(tree)

    # Set the words at the leaves of a tree to the words from the list
    def set_words(self, words):
        self.set_words_helper(words, 0)

    def set_words_helper(self, words, word_num):
        if self.is_leaf():
            self.label = words[word_num]
            return word_num + 1
        else:
            for child in self.children:
                word_num = child.set_words_helper(words, word_num)
            return word_num

    def to_sub_tree_list(self):
        return self.get_pre_order_traversal()

    # Creates a list of all constituents in this tree. A constituent
    # is just a non-terminal label and that non-terminal covers in the tree.
    def to_constituent_list(self):
        constituent_list = []
        self.to_constituent_list_collection_helper(self, 0, constituent_list)
        return constituent_list

    def to_constituent_list_collection_helper(self, tree, start, constituents):
        if tree.is_leaf() or tree.isPreTerminal():
            return 1
        span = 0
        for child in tree.children:
            span += self.to_constituent_list_collection_helper(child, start + span, constituents)
        constituents.append(Constituent(tree.label, start, start + span))
        return span

    @staticmethod
    def from_string(string):
        lines = string.split('\n')
        return Tree.from_string_helper(lines)

    @staticmethod
    def from_string_helper(lines, last_parent=None):
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
    def to_string(self):
        string = '\t' * self.indent
        if not self.is_leaf():
            string += '('
        if self.label is not None:
            string += self.label + ',' + str(self.line) + ',' + str(self.indent)
        if not self.is_leaf():
            for child in self.children:
                string += '\n' + child.to_string()
            string += ')'
        return string

    def deep_copy(self, tree=None):
        if tree is None: return self.deep_copy(self)

        children_copies = []
        for child in self.children:
            children_copies.append(self.deep_copy(child))
        return Tree(tree.getLabel(), children_copies)
