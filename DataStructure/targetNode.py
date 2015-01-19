from __future__ import print_function
import os

__author__ = 'Marouane'


class TargetNode(object):
    def __init__(self, value='', command='', parent=None, dependencies=[]):
        self.value = value
        self.parent = parent
        self.dependencies = dependencies
        self.command = command
        self.state = 0
        self.child_count = 0
        self.satisfied = False

    def add_dependence(self, dependence):
        self.dependencies.append(dependence)

    def cut_dependencies(self):
        for ep in self.dependencies:
            dep = None

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

    def update_satisfaction(self):
        satisfaction = True
        for node in self.dependencies:
            if not node.satisfied:
                satisfaction = False
                break

        if satisfaction:
            self.satisfied = True
