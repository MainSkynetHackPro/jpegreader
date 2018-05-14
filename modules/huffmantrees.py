from modules.huffmantree import HuffmanTree


class HuffmanTrees:
    """
    Container for all huffman tree nodes
    add(..) adds string with huffman tree
    build(..) builds each tree
    """
    def __init__(self):
        self.trees = []

    def add(self, tree_string):
        self.trees.append(HuffmanTree(tree_string))

    def build(self):
        for tree in self.trees:
            tree.build()
