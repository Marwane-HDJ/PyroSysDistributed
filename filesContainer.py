# saved as filesContainer.py
__author__ = 'monssef'

#dictionnary which contains the current files
class FilesContainer(object):
    def __init__(self):
        self.files = {}

    def list_files(self):
        return self.files

    def store(self, name):
        fileContent = open(name, "r")
        self.files[name] = fileContent.read()
        fileContent.close()

    def take(self, name):
        return self.files.pop(name)