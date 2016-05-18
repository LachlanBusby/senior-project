import itertools

class TreeAnnotations:

	def annotateTree(self, unAnnotatedTree):
		return self.binarizeTree(unAnnotatedTree)

	def secondOrderVerticalMarkov(self, parentLabel, tree):
		if tree.isLeaf(): return
		currLabel = tree.getLabel()
		if parentLabel != None:
			tree.setLabel(currLabel + "^" + parentLabel)
		for childTree in tree.getChildren():
			self.secondOrderVerticalMarkov(currLabel, childTree)

	def binarizeTree(self, tree):
		label = tree.getLabel()
		if tree.isLeaf():
			return Tree(label)
		if len(tree.getChildren()) == 1:
			return Tree(label, [self.binarizeTree(tree.getChildren()[0])])
		intermediateLabel = "@" + label + "->"
		intermediateTree = self.binarizeTreeHelper(tree, 0, intermediateLabel)
		return Tree(label, intermediateTree.getChildren())

	def binarizeTreeHelper(self, tree, numChildrenGenerated, intermediateLabel):
		leftTree = tree.getChildren()[numChildrenGenerated]
		children = []
		children.append(self.binarizeTree(leftTree))
		if numChildrenGenerated < len(tree.getChildren()) - 1:
			rightTree = self.binarizeTreeHelper(tree, numChildrenGenerated + 1, intermediateLabel + "_" + leftTree.getLabel())
			children.append(rightTree)
		return Tree(intermediateLabel, children)

	def unAnnotateTree(self, annotatedTree):
		debinarizedTree = Trees.spliceNodes(annotatedTree, lambda s: s.startswith('@'))
		unAnnotatedTree = Trees.FunctionnodesStripper().transformTree(debinarizedTree)
		unMarkovizedTree = Trees.MarkovizationAnnotationStripper().transformTree(unAnnotatedTree)
		return unMarkovizedTree
