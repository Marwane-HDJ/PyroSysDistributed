from __future__ import print_function
import os
import Pyro4

__author__ = 'Marouane'

# Pyro4.config.REQUIRE_EXPOSE = True

@Pyro4.expose
class TargetNode(object):
    def __init__(self, value='', command='', parent=None, dependencies=None):
        if not dependencies:
            dependencies = []
        self.value = value
        self.parent = parent
        self.dependencies = dependencies
        self.command = command
        self.state = 0
        self.child_count = 0
        self.satisfied = False
        self.exist = False
        self.file_dependencies = []

    def add_dependence(self, dependence):
        self.dependencies.append(dependence)

    def remove_dependence(self, dependence):
        self.dependencies.remove(dependence)

    def add_file_dependence(self, dependence):
        self.file_dependencies.append(dependence)

    def remove_file_dependence(self, dependence):
        self.file_dependencies.remove(dependence)

    def cut_dependencies(self):
        for ep in self.dependencies:
            dep = None

    def set_command(self, command):
        self.command = command

    def set_parent(self, parent):
        self.parent = parent

    def get_value(self):
        return self.value

    def get_dependencies(self):
        return self.dependencies

    def get_file_dependencies(self):
        return self.file_dependencies

    def get_command(self):
        return self.command

    # @Pyro4.expose
    def set_value(self, value):
        self.value = value

    def execute_command(self):
        if len(self.command) != 0:
            os.system(self.command)

    def print_dependencies(self):
        for dependence in self.dependencies:
            print(dependence.value + "\n")

    def update_satisfaction(self):
        satisfaction = True
        for node in self.dependencies:
            if not node.satisfied:
                satisfaction = False
                break

        if satisfaction:
            self.satisfied = True

