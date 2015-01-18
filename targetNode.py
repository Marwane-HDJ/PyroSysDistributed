import os

__author__ = 'Marouane'


class TargetNode(object):
    def __init__(self, value='', command='', parent=None, dependencies=[]):
        self.value = value
        self.parent = parent
        self.dependencies = dependencies
        self.command = command
        self.satisfied = False
        self.child_count = 0

    def add_dependence(self, dependence):
        self.dependencies.append(dependence)

    def set_command(self, command):
        self.command = command

    def set_parent(self, parent):
        self.parent = parent

    def execute_command(self):
        if len(self.command) != 0:
            os.system(self.command)

    def print_dependencies(self):
        for dependence in self.dependencies:
            print(dependence.value + "\n")
