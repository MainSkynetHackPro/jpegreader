class AcDcMatrix:
    def __init__(self, huffman_trees, scan_params, img_body):
        self.huffman_trees = huffman_trees
        self.scan_params = scan_params
        self.img_body = bin(int(img_body, 16))[2:]
        self.matrix = []

