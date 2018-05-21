from modules.decoder.imagechunk import ImageChunk


class Decoder:
    def __init__(self, parsed_image, huffman_tables, dqt_tables):
        self.huffman_tables = huffman_tables
        self.parsed_image = parsed_image
        self.image_body = bin(int(self.parsed_image.start_of_scan_body, 16))[2:]  # convert to binary
        self.dqt_tables = dqt_tables
        self.chunks = []

    def decode(self):
        offset = 0

        while int(offset) < int(len(self.image_body)):
            chunk = ImageChunk(self.parsed_image, self.huffman_tables)
            chunk_len = chunk.load(self.image_body[offset:])
            chunk.calculate()
            offset += chunk_len
            exit()
