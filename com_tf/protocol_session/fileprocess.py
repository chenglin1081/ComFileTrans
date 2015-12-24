# -*- coding: utf-8 -*-

import os


class FileBase:
    def __init__(self):
        self.file = None
        self.size = 0

    def close(self):
        self.file.close()

    def __len__(self):
        return self.size

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class FileWriter(FileBase):
    def __init__(self, fullname):
        super(FileWriter, self).__init__()
        self.file = open(fullname, 'ab')
        self.size = os.path.getsize(fullname)

    def truncate(self, size):
        self.flush()
        if size < self.size:
            self.file.truncate(size)
            self.size = size

    def write(self, stream):
        self.size += len(stream)
        self.file.write(stream)

    def flush(self):
        self.file.flush()


class FileReader(FileBase):
    def __init__(self, fullname):
        super(FileReader, self).__init__()
        self.file = open(fullname, 'rb')
        self.size = os.path.getsize(fullname)

    def read(self, index=0, size=None):
        left = len(self) - index
        if left > 0:
            size = min(left, size) if size else left
            self.file.seek(index)
            return self.file.read(size)
