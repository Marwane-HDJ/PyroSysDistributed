import sys
from os.path import abspath, exists
from parser import parse, print_make_file
from targetNode import TargetNode

__author__ = 'Marouane'


class TargetTree(object):
    def __init__(self, makefile):
        self.tree_root = None
        self.targets = {}
        self.first = True

        for target in makefile:
            p = None

            if not self.targets.has_key(target.value):
                p = TargetNode(target.value, target.commands, None, [])
                self.targets.update({target.value: p})
            else:
                p = self.targets.get(target.value)
                p.set_command(target.commands)
                self.targets.update({target.value: p})

            if self.first:
                self.tree_root = self.targets.get(target.value)
                self.first = False

            for dependence in target.dependencies:
                d = None
                if not self.targets.has_key(dependence):
                    d = TargetNode(dependence, '', p, [])
                    p.add_dependence(d)
                    self.targets.update({dependence: d})
                else:
                    d = self.targets.get(dependence)
                    p.add_dependence(d)

    def print_dico(self):
        for key in self.targets:
            print("Node : " + key + "\n")
            obj = self.targets.get(key)
            print(obj.command)
            print("\n")
            if len(obj.dependencies) > 0:
                print("Dependencies : ")
                for val in obj.dependencies:
                    print(val.value + " ")
                print("\n")

    def recursive_execute(self, node):
        if len(node.dependencies) == 0:
            if len(node.command) != 0:
                # TODO : Change from print to execute
                print(node.command)
        else:
            for dep in node.dependencies:
                self.recursive_execute(dep)
                # if len(dep.command) > 0:
                # print(dep.command)
            # TODO : Change from print to execute
            print(node.command)


def main():
    if 2 != len(sys.argv):
        print("Arguments incorrects")
        # TODO : refactor with exceptions
    else:
        f_path = abspath(sys.argv[1])
        makefile = parse(f_path)
        # print_make_file(makefile)
        tree = TargetTree(makefile)
        # tree.print_dico()
        tree.recursive_execute(tree.tree_root)


if __name__ == "__main__":
    main()


