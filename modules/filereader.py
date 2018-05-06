import binascii

TWO_BYTE_STEP_LEN = 4
ONE_BYTE_STEP_LEN = 2


class FileReader:
    """
    File reader object reads file in byte mode
    Can convert byte string to hex
    """
    def __init__(self, filename):
        self.filename = filename
        self.file_data = None
        self.file_chunks = []

    def read(self):
        filestream = open(self.filename, 'rb')
        for chunk in iter(lambda: filestream.read(16), b''):
            self.file_chunks.append(chunk)

    def hexify(self):
        self.file_chunks = map(lambda x: binascii.hexlify(x), self.file_chunks)

    def two_byte_iterator(self):
        for row in self.file_chunks:
            for index in range(0, len(row), ONE_BYTE_STEP_LEN):
                yield row[index:index + ONE_BYTE_STEP_LEN]
