from tree import Tree


class Trees:

    class FunctionNodeStripper:
        def transform_tree(self, tree):
            transformed_label = tree.label
            cut_index = transformed_label.index('-') if '-' in transformed_label else -1
            cut_index2 = transformed_label.index('=') if '=' in transformed_label else -1
            if cut_index2 > 0 and (cut_index2 < cut_index or cut_index == -1):
                cut_index = cut_index2
            if cut_index > 0 and not tree.is_leaf():
                transformed_label = transformed_label[:cut_index]
            if tree.is_leaf():
                return Tree(transformed_label)
            transformed_children = []
            for child in tree.children:
                transformed_children.append(self.transform_tree(child))

            return Tree(transformed_label, transformed_children)

    class MarkovizationAnnotationStripper:
        def transform_tree(self, tree):
            transformed_label = tree.label
            caret_index = transformed_label.index('^') if '^' in transformed_label else -1
            if caret_index > 0:
                transformed_label = transformed_label[:caret_index]
            if tree.is_leaf():
                return Tree(transformed_label)
            transformed_children = []
            for child in tree.children:
                transformed_children.append(self.transform_tree(child))
            return Tree(transformed_label, transformed_children)

    class EmptyNodeStripper:
        def transform_tree(self, tree):
            label = tree.label
            if label == '-NONE-':
                return None
            if tree.is_leaf():
                return Tree(label)
            transformed_children = []
            for child in tree.children:
                transformed_child = self.transform_tree(child)
                if transformed_child is not None:
                    transformed_children.append(transformed_child)
            if len(transformed_children) == 0:
                return None
            return Tree(label, transformed_children)

    class XOverXRemover:
        def transform_tree(self, tree):
            label = tree.label
            children = tree.children
            while len(children) == 1 and not children[0].is_leaf() and label == children[0].label:
                children = children[0].children
            transformed_children = []
            for child in children:
                transformed_children.append(self.transform_tree(child))
            return Tree(label, transformed_children)

    class StandardTreeNormalizer:
        def __init__(self):
            self.emptyNodeStripper = EmptyNodeStripper()
            self.xOverXRemover = XOverXRemover()
            self.functionNodeStripper = FunctionNodeStripper()

        def transform_tree(self, tree):
            tree = self.functionNodeStripper.transform_tree(tree)
            tree = self.emptyNodeStripper.transform_tree(tree)
            tree = self.xOverXRemover.transform_tree(tree)
            return tree

    # class TreeReader:
    # SKIPPING THIS CLASS FOR NOW

    # SKIPPING EVERYTHING AFTER TREE_READER CLASS EXCEPT SPLICE_NODES

    def splice_nodes(self, tree, filtr):
        root_list = self.splice_nodes_helper(tree, filtr)
        if len(root_list) > 1:
            raise Exception('spliceNodes: no unique root after splicing')
        if len(root_list) < 1:
            return None
        return root_list[0]

    def splice_nodes_helper(self, tree, filtr):
        spliced_children = []
        for child in tree.children:
            spliced_child_list = self.splice_nodes_helper(child, filtr)
            spliced_children.extend(spliced_child_list)

        if filtr(tree.label):
            return spliced_children
        return [Tree(tree.label, spliced_children)]

    # SKIPPING FURTHER FUNCTIONS UNTIL PROVEN NECESSARY
