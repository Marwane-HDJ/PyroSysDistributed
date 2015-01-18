__author__ = 'Marouane'

from os.path import abspath
import sys
from Utilities.parser import print_make_file, parse


def main():
    if 2 != len(sys.argv):
        print("Arguments incorrects")
        # TODO : refactor with exceptions
    else:
        f_path = abspath(sys.argv[1])
        makefile = parse(f_path)
        print_make_file(makefile)


if __name__ == "__main__":
    main()