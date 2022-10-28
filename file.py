class File:
    def __init__(self, file_path, size, file_hash):
        self.file_path = file_path
        self.size = size
        self.file_hash = file_hash

    def compare(self, file):
        if self.file_path == file.file_path and self.file_hash == file.file_hash:
            return True
        return False
