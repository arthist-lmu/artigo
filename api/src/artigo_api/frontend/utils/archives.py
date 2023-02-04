import tarfile
import zipfile


class Archive:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file = None

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        self.file.close()
        self.file = None


class TarArchive(Archive):
    def __enter__(self):
        self.file = tarfile.open(self.file_path, mode='r')

        return self

    def members(self):
        if self.file is None:
            return []
        else:
            for info in self.file.getmembers():
                yield info.name

    def read(self, name):
        if self.file is None:
            return None

        try:
            return self.file.extractfile(name).read()
        except KeyError:
            return None


class ZipArchive(Archive):
    def __enter__(self):
        self.file = zipfile.ZipFile(self.file_path, 'r')

        return self

    def members(self):
        if self.file is None:
            return []
        else:
            for name in self.file.namelist():
                yield name

    def read(self, name):
        if self.file is None:
            return None

        try:
            return self.file.open(name).read()
        except KeyError:
            return None
