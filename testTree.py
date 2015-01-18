__author__ = 'Marouane'

from Utilities.parser import parse
from os.path import abspath
import sys
from DataStructure.targetTree import TargetTree


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
