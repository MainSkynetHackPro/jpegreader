from modules.dqt import DQT
from modules.filereader import FileReader
from modules.huffmantrees import HuffmanTrees
from modules.imageparser import ImageParser


class ImageReader:
    """
    Base class. Is responsible fot managing other modules.
    process_image function
    todo: should return rgb matrix (representing image)
    """
    def __init__(self, filename):
        self.filereader = FileReader(filename)
        self.parsed_image = None
        self.huffman_trees = HuffmanTrees()
        self.dqt_list = {}

    def process_image(self):
        self.read_image()
        image_parser = ImageParser(self.filereader.two_byte_iterator())
        self.parsed_image = image_parser.parse()
        self.load_dqt()
        self.build_huffman_trees()

    def read_image(self):
        self.filereader.read()
        self.filereader.hexify()

    def load_dqt(self):
        for i in self.parsed_image.quant_tables:
            self.dqt_list[i] = DQT(self.parsed_image.quant_tables[i])

    def build_huffman_trees(self):
        for item in self.parsed_image.huffman_tables:
            self.huffman_trees.add(item)
        self.huffman_trees.build()
