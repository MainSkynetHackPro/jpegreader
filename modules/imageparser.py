START_MARKER = b'ffd8'
COMMENTS_MARKER = b'fffe'
QUANT_TABLE_MARKER = b'ffdb'
CODING_PARAM_MARKER = b'ffc0'
HUFFMAN_TABLE_MARKER = b'ffc4'
START_OF_SCAN_MARKER = b'ffda'
END_FILE_MARKER = b'ffd9'

BYTE_LEN_IN_SYMBOLS = 2


class ImageParser:
    """
    HEX image parser
    parse function returns ParsedImage object, which contains sections of image file
    """

    def __init__(self, iterator):
        self.iterator = iterator
        self.parsed_image = ParsedImage()

    def parse(self):
        for chunk in self.iterator:
            marker = chunk + self.get_one_byte()
            self.get_marker_handler(marker)
        self.parsed_image.parse_image_params()
        return self.parsed_image

    def get_marker_handler(self, marker):
        """
        Fills ParsedImage object with sections
        each function handles it's own section
        :param marker:
        """

        def comment_handler(section):
            self.parsed_image.comment = section

        def quant_table_handler(section):
            table_id = int(section[:2])
            self.parsed_image.quant_tables[table_id] = section[2:]

        def coding_param_handler(section):
            self.parsed_image.coding_param = section

        def huffman_table_handler(section):
            table_id = int(section[:2])
            self.parsed_image.huffman_tables[table_id] = section[2:]

        def start_of_scan_handle(section):
            self.parsed_image.start_of_scan_header = section
            for item in self.iterator:
                self.parsed_image.start_of_scan_body += item
            if self.parsed_image.start_of_scan_body[-4:] == END_FILE_MARKER:
                self.parsed_image.start_of_scan_body = self.parsed_image.start_of_scan_body[:-4]

        # byte-handler map
        handler_map = {
            COMMENTS_MARKER: comment_handler,
            QUANT_TABLE_MARKER: quant_table_handler,
            CODING_PARAM_MARKER: coding_param_handler,
            HUFFMAN_TABLE_MARKER: huffman_table_handler,
            START_OF_SCAN_MARKER: start_of_scan_handle,
        }
        try:
            handler_map[marker](self.load_section())
        except KeyError:
            pass

    def get_two_bytes(self):
        return self.get_one_byte() + self.get_one_byte()

    def get_one_byte(self):
        try:
            return self.iterator.__next__()
        except StopIteration:
            return b''

    def load_section(self):
        """
        reads section from FileParser object
        :return: separate section (size is specified in first 2 bytes)
        """
        section_string = b''
        section_lenght = int(self.get_two_bytes(), 16)
        for byte in range(0, int(section_lenght) - 2):
            new_str = self.get_one_byte()
            section_string += new_str
        return section_string


COMPONENT_PARAMS_LENGTH = 6


class ParsedImage:
    """
    Object of this class contains information of image file
    """
    comment = b''
    quant_tables = {}
    coding_param = b''
    huffman_tables = {}
    start_of_scan_header = b''
    start_of_scan_body = b''
    params = {}

    def parse_image_params(self):
        """
        parses coding params:
        - image width and height
        - components count
        - vertical and horizontal dithering, dqt index for each color component
        """
        params = self.coding_param.decode("utf-8")
        self.params = {
            'precision': int(params[0:2]),
            'height': int(params[2:6]),
            'width': int(params[6:10]),
            'components': {}
        }
        offset = 10
        for i in range(0, 3):
            current_offset = offset + COMPONENT_PARAMS_LENGTH * i + 1
            print(current_offset)
            self.params['components'][int(params[current_offset: current_offset + 1])] = {
                'h': int(params[current_offset + 2]),
                'v': int(params[current_offset + 3]),
                'dqt': int(params[current_offset + 4: current_offset + 5])
            }
