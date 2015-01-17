__author__ = 'Marouane'


class Target(object):
    def __init__(self, value, command):
        self.value = value
        self.commands = command
        self.isfinal = True

    def __init__(self, value, dependencies, command):
        self.value = value
        self.dependencies = dependencies
        self.commands = command
        if 0 == len(dependencies):
            self.isfinal = True
        else:
            self.isfinal = False

    def __init__(self, value, parent, command, dependences):
        self.value = value
        self.parent = parent
        self.dependencies = dependences
        self.commands = command

    def getdependenciestostring(self):
        return " ".join(self.dependencies)

