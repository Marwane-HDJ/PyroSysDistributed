__author__ = 'Marouane'


class Target(object):
    def __init__(self, value, dependencies, commands):
        self.value = value
        self.dependencies = dependencies
        self.commands = commands
        if 0 == len(dependencies):
            self.isfinal = True
        else:
            self.isfinal = False

    def getdependenciestostring(self):
        return " ".join(self.dependencies)