class Trees:

    class FunctionNodeStripper:
        def transformTree(self, tree):
            transformedLabel = tree.getLabel()
            cutIndex = transformedLabel.index('-') if '-' in transformedLabel else -1
            cutIndex2 = transformedLabel.index('=') if '=' in transformedLabel else -1
            if cutIndex2 > 0 and (cutIndex2 < cutIndex or cutIndex == -1):
                cutIndex = cutIndex2
            if cutIndex > 0 and not tree.isLeaf():
                transformedLabel = transformedLabel[:cutIndex]
            if tree.isLeaf():
                return Tree(transformedLabel)
            transformedChildren = []
            for child in tree.getChildren():
                transformedChildren.append(self.transformTree(child))

            return Tree(transformedLabel, transformedChildren)

    class MarkovizationAnnotationStripper:
        def transformTree(self, tree):
            transformedLabel = tree.getLabel()
            caretIndex = transformedLabel.index('^') if '^' in transformedLabel else -1
            if caretIndex > 0:
                transformedLabel = transformedLabel[:caretIndex]
            if tree.isLeaf():
                return Tree(transformedLabel)
            transformedChildren = []
            for child in tree.getChildren():
                transformedChildren.append(self.transformTree(child))
            return Tree(transformedLabel, transformedChildren)

    class EmptyNodeStripper:
        def transformTree(self, tree):
            label = tree.getLabel()
            if label == '-NONE-':
                return None
            if tree.isLeaf():
                return Tree(label)
            transformedChildren = []
            for child in tree.getChildren():
                transformedChild = self.transformTree(child)
                if transformedChild is not None:
                    transformedChildren.append(transformedChild)
            if len(transformedChildren) == 0:
                return None
            return Tree(label, transformedChildren)

    class XOverXRemover:
        def transformTree(self, tree):
            label = tree.getLabel()
            children = tree.getChildren()
            while len(children) == 1 and not children[0].isLeaf() and label == children[0].getLabel():
                children = children[0].getChildren()
            transformedChildren = []
            for child in children:
                transformedChildren.append(self.transformTree(child))
            return Tree(label, transformedChildren)

    class StandardTreeNormalizer:
        def __init__(self):
            self.emptyNodeStripper = EmptyNodeStripper()
            self.xOverXRemover = XOverXRemover()
            self.functionNodeStripper = FunctionNodeStripper()

        def transformTree(self, tree):
            tree = self.functionNodeStripper.transformTree(tree)
            tree = self.emptyNodeStripper.transformTree(tree)
            tree = self.xOverXRemover.transformTree(tree)
            return tree

    # class TreeReader:
    # SKIPPING THIS CLASS FOR NOW

    # SKIPPING EVERYTHING AFTER TREE_READER CLASS EXCEPT SPLICE_NODES

    def spliceNodes(self, tree, filtr):
        rootList = self.spliceNodesHelper(tree, filtr)
        if len(rootList) > 1:
            raise Exception('spliceNodes: no unique root after splicing')
        if len(rootList) < 1:
            return None
        return rootList[0]

    def spliceNodesHelper(self, tree, filtr):
        splicedChildren = []
        for child in tree.getChildren():
            splicedChildList = self.spliceNodesHelper(child, filtr)
            splicedChildren.extend(splicedChildList)

        if filtr(tree.getLabel()):
            return splicedChildren
        return [Tree(tree.getLabel(), splicedChildren)]

    # SKIPPING FURTHER FUNCTIONS UNTIL PROVEN NECESSARY
