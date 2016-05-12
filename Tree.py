#!/usr/bin/python

class Tree:
	'''Represent linguistic trees, with each node consisting of a label
	and a list of children.
	Original Java Code by Dan Klein.'''

	# The leaf constructor
	def __init__(self, label, indent, children=[], parent=None):
		self.label = label
		self.indent = indent
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

	# Returns true at the word(leaf) level of a tree
	def isLeaf(self):
		return not self.children


	# Returns true level of non-terminals which are directly above
	# single words(leafs)
	def isPreTerminal(self):
		return len(self.children) == 1 and self.children[0].isLeaf()


	def isPhrasal(self):
		return not (self.isLeaf() or self.isPreTerminal())


	# Returns a list of words at the leafs of this tree gotten by
	# traversing from left to right
	def getYield(self):
		yield_list = []
		self.appendYield(self, yield_list)
		return yield_list

	def appendYield(self, tree, yield_list):
		if tree.isLeaf():
			yield_list.append(tree.getLabel())
			return
		for child in tree.getChildren():
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


	# Returns a string representation of this tree using bracket notation.
	def toString(self):
		string = ''
		self.toStringHelper(string)
		return string

	def toStringHelper(self, string):
		if not self.isLeaf():
			string +='('
		if self.getLabel() != None:
			string += self.getLabel()
		if not self.isLeaf():
			for child in self.children:
				string += ' '
				child.toStringHelper(string)
			string += ')'

	def deepCopy(self, tree=None):
		if tree is None: return deepCopy(self)

		childrenCopies = []
		for child in self.children:
			childrenCopies.append(deepCopy(child))
		return Tree(tree.getLabel(), childrenCopies)
