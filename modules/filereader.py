import binascii

TWO_BYTE_STEP_LEN = 4
ONE_BYTE_STEP_LEN = 2


class FileReader:
    """
    File reader object reads file in byte mode
    Can convert byte string to hex
    """
    def __init__(self, filename):
        self.__filename = filename
        self.__file_data = None
        self.__file_chunks = []

    def read(self):
        filestream = open(self.__filename, 'rb')
        for chunk in iter(lambda: filestream.read(16), b''):
            self.__file_chunks.append(chunk)

    def hexify(self):
        self.__file_chunks = map(lambda x: binascii.hexlify(x), self.__file_chunks)

    def two_byte_iterator(self):
        for row in self.__file_chunks:
            for index in range(0, len(row), ONE_BYTE_STEP_LEN):
                yield row[index:index + ONE_BYTE_STEP_LEN]
