__author__ = 'Marouane'


class Target(object):
    def __init__(self, value, dependencies, command):
        self.value = value
        self.dependencies = dependencies
        self.commands = command

    def dependencies_to_string(self):
        return " ".join(self.dependencies)

