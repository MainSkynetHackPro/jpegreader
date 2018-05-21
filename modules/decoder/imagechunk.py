from modules.utils.zigzagmatrix import ZigZagMatrix


class ImageChunk:
    def __init__(self, parsed_image, huffman_tables):
        self.huffman_tables = huffman_tables
        self.parsed_image = parsed_image
        self.matrix = {}

        for item, value in parsed_image.inv_decimation.items():
            dimensions = value['h'] * value['v']
            matrix_list = []
            for i in range(dimensions):
                matrix_list.append(ZigZagMatrix())
            self.matrix[item] = matrix_list

    def load(self, img_body):
        offset = 0
        for c_key, component in self.matrix.items():
            for sub_component in component:
                offset += self.fill_matrix(img_body[offset:], sub_component,
                                           self.parsed_image.start_of_scan_params[c_key])
            self.fix_dc(c_key)
        return offset

    def calculate(self):
        pass

    def fill_matrix(self, img_body, matrix, huffman_indexes):
        huffman_table_ac = self.huffman_tables.trees[f'{huffman_indexes["ac"]}AC']
        huffman_table_dc = self.huffman_tables.trees[f'{huffman_indexes["dc"]}DC']
        dc_val, offset = self.find_el_in_string_dc(img_body, huffman_table_dc)
        if not dc_val == -1:
            matrix.put(dc_val)
        else:
            matrix.put(0)
        for i in range(0, 63):
            ac_val_list, inc_offset = self.find_el_in_string_ac(img_body[offset:], huffman_table_ac)
            offset += inc_offset
            if ac_val_list == -1:
                return offset
            for i in ac_val_list:
                matrix.put(i)
        return offset

    def find_el_in_string_dc(self, img_body, huffman_table):
        for index in range(0, huffman_table.max_key_length + 1):
            if img_body[0: index] in huffman_table.huffman_table:
                key = img_body[0: index]
                huffman_value = int(huffman_table.huffman_table[key], 16)
                if huffman_value == 0:
                    return -1, -1
                item = int(img_body[index: index + huffman_value], 2)
                binary_value = bin(item)[2:]
                if int(binary_value[0]) == 0:
                    item = item - 2 ** len(str(binary_value)) + 1
                return item, index + huffman_value

    def find_el_in_string_ac(self, img_body, huffman_table):
        for index in range(0, huffman_table.max_key_length + 1):
            if img_body[0: index] in huffman_table.huffman_table:
                key = img_body[0: index]
                huffman_value = huffman_table.huffman_table[key]

                if int(huffman_value, 16) == 0:
                    return -1, index

                zeroes = int(huffman_value[0:1], 16)
                read_items = int(huffman_value[1:2], 16)
                items = []
                for i in range(zeroes):
                    items.append(0)
                item = int(img_body[index: index + read_items], 2)
                binary_value = bin(item)[2:]
                if int(binary_value[0]) == 0:
                    item = item - 2 ** len(str(binary_value)) + 1
                items.append(item)
                return items, index + read_items
        return -1, 0

    def fix_dc(self, c_key):
        for i in range(0, len(self.matrix[c_key])):
            if i > 0:
                self.matrix[c_key][i].set(0, 0, self.matrix[c_key][i].get(0, 0) + self.matrix[c_key][i - 1].get(0, 0))
