#!/usr/bin/env python
from modules.imagereader import ImageReader

if __name__ == '__main__':
    freader = ImageReader('images/test.jpg')
    freader.process_image()
