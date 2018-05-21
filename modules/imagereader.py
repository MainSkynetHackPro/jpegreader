from modules.decoder.decoder import Decoder
from modules.imageprocessing.dqt import DQT
from modules.filereader.filereader import FileReader
from modules.huffman.huffmantrees import HuffmanTrees
from modules.filereader.imageparser import ImageParser


class ImageReader:
    """
    Base class. Is responsible fot managing other modules.
    todo: should return rgb matrix (representing image)
    """
    def __init__(self, filename):
        self.filereader = FileReader(filename)
        self.parsed_image = None
        self.huffman_trees = HuffmanTrees()
        self.dqt_tables = {}

    def process_image(self):
        self.read_image()
        image_parser = ImageParser(self.filereader.two_byte_iterator())
        self.parsed_image = image_parser.parse()
        self.load_dqt()
        self.build_huffman_trees()
        img_decoder = Decoder(self.parsed_image, self.huffman_trees, self.dqt_tables)
        img_decoder.decode()

    def read_image(self):
        self.filereader.read()
        self.filereader.hexify()

    def load_dqt(self):
        for i in self.parsed_image.quant_tables:
            self.dqt_tables[i] = DQT(self.parsed_image.quant_tables[i])

    def build_huffman_trees(self):
        for item in self.parsed_image.huffman_tables:
            self.huffman_trees.add(item)
        self.huffman_trees.build()
