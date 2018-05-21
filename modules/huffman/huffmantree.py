CODES_OFFSET = 16 * 2
HUFFMAN_TABLE_INDEX_OFFSET = 1 * 2


class TreeNode:
    def __init__(self, value=None, parent=None, index=None, code_len=0, right=False):
        self.value = value
        self.parent = parent
        self.l_child = None
        self.r_child = None
        self.index = index
        self.code_len = code_len
        if not self.parent:
            self.code = ''
        else:
            if right:
                self.code = self.parent.code + '1'
            else:
                self.code = self.parent.code + '0'

    def is_head(self):
        return not bool(self.parent)

    def has_left_child(self):
        return bool(self.l_child)

    def has_right_child(self):
        return bool(self.r_child)

    def has_both_children(self):
        return self.has_right_child() and self.has_left_child()


class HuffmanTree:
    """
    Huffman tree. Builds tree from string
    """

    def __init__(self, huffman_string):
        self.huffman_string = huffman_string
        self.codes = self.get_codes()
        self.values = self.get_values()
        self.tree_head = TreeNode(code_len=0)
        self.pointer = self.tree_head
        self.huffman_table = {}
        self.max_key_length = 0

    def build(self):
        def len_generator(codes_list):
            for item_index in range(0, len(codes_list)):
                while codes_list[item_index] != 0:
                    yield item_index + 1
                    codes_list[item_index] -= 1

        code_len = len_generator(self.codes)
        for index, value in enumerate(self.values):
            pointer = self.insert_node(value, next(code_len))
            self.huffman_table[pointer.code] = pointer.value
            self.max_key_length = max(len(pointer.code), self.max_key_length)

    def get_codes(self):
        codes = []
        for index in range(HUFFMAN_TABLE_INDEX_OFFSET, CODES_OFFSET, 2):
            codes.append(int(self.huffman_string[index: index + 2], 16))
        return codes

    def get_values(self):
        values = []
        for index in range(CODES_OFFSET + 2, len(self.huffman_string), 2):
            values.append(self.huffman_string[index: index + 2])
        return values

    def insert_node(self, value, code_len):
        if self.pointer.has_both_children():
            self.pointer = self.pointer.parent
            return self.insert_node(value, code_len)
        if self.pointer.code_len + 1 == code_len:
            if not self.pointer.has_left_child():
                self.pointer.l_child = TreeNode(parent=self.pointer, value=value, code_len=code_len, right=False)
                return self.pointer.l_child
            elif self.pointer.has_left_child() and not self.pointer.has_right_child():
                self.pointer.r_child = TreeNode(parent=self.pointer, value=value, code_len=code_len, right=True)
                return self.pointer.r_child
        elif self.pointer.code_len < code_len:
            if not self.pointer.has_left_child():
                self.pointer.l_child = TreeNode(parent=self.pointer, code_len=self.pointer.code_len + 1, right=False)
                self.pointer = self.pointer.l_child
            elif self.pointer.has_left_child() and not self.pointer.has_right_child():
                self.pointer.r_child = TreeNode(parent=self.pointer, code_len=self.pointer.code_len + 1, right=True)
                self.pointer = self.pointer.r_child
            return self.insert_node(value, code_len)
