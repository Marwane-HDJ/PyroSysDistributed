# saved as filesContainer.py
import Pyro4

__author__ = 'monssef'

# dictionnary which contains the current files

Pyro4.config.REQUIRE_EXPOSE = True


@Pyro4.expose
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
        return self.files[name]