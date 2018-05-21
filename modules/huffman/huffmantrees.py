from .huffmantree import HuffmanTree


class HuffmanTrees:
    """
    Container for all huffman tree nodes
    add(..) adds string with huffman tree
    build(..) builds each tree
    """
    def __init__(self):
        self.trees = {}

    def add(self, tree_string):
        ac_dc = int(tree_string[0:1], 16)
        index = int(tree_string[1:2], 16)
        if ac_dc == 1:
            ac_dc_str = 'AC'
        else:
            ac_dc_str = 'DC'
        self.trees[f'{index}{ac_dc_str}'] = HuffmanTree(tree_string)

    def build(self):
        for key in self.trees:
            self.trees[key].build()
