from modules.filereader import FileReader
from modules.imageparser import ImageParser


class ImageReader:
    """
    Base class. Is responsible fot managing other modules.
    process_image function
    todo: should return rgb matrix (representing image)
    """
    def __init__(self, filename):
        self.__filereader = FileReader(filename)
        self.parsed_image = None

    def process_image(self):
        self.__read_image()
        image_parser = ImageParser(self.__filereader.two_byte_iterator())
        self.parsed_image = image_parser.parse()

    def __read_image(self):
        self.__filereader.read()
        self.__filereader.hexify()
