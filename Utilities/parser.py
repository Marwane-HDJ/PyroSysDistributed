__author__ = 'Marouane'

import sys
import re
from os.path import abspath, exists

from Utilities.target import Target


def parse(f_path):
    regexpcomment = re.compile("^#.*")
    regexpcommand = re.compile("^\\t.*")
    regexptrgtdep = re.compile("^.+:.*")
    lastintargetdep = False
    lastincommand = False
    targets = list()
    commands = list()
    target = None

    if exists(f_path):
        file_object = open(f_path, 'rU')
        try:
            for line in file_object:
                line = line.rstrip()
                if line:
                    if not regexpcomment.search(line):
                        if regexptrgtdep.match(line):
                            if lastincommand and target:
                                target.commands = commands
                                commands = list()
                                targets.append(target)
                                lastincommand = False
                            lastintargetdep = True
                            x = line.split(":", 1)
                            target = Target(x[0], x[1].strip().split(), None)
                        elif regexpcommand.match(line):
                            if lastintargetdep or lastincommand:
                                lastintargetdep = False
                                lastincommand = True
                                commands.append(line)
                            else:
                                # TODO : refactor with exception for invalid make file
                                print("Invalid make file 1")
                                sys.exit(1)
                        else:
                            # TODO : refactor with exception for invalid make file
                            print("Invalid make file 2")
                            sys.exit(1)
            if target:
                target.commands = commands
                targets.append(target)

        finally:
            file_object.close()
            return targets


def parse_v2(f_path):
    regexpcomment = re.compile("^#.*")
    regexpcommand = re.compile("^\\t.*")
    regexptrgtdep = re.compile("^.+:.*")
    lastintargetdep = False
    lastincommand = False
    targets = list()
    commands = list()
    target = None

    if exists(f_path):
        file_object = open(f_path, 'rU')
        try:
            for line in file_object:
                line = line.rstrip()
                if line:
                    if not regexpcomment.search(line):
                        if regexptrgtdep.match(line):
                            if target:
                                target.commands = commands
                                commands = list()
                                targets.append(target)
                                lastincommand = False
                            lastintargetdep = True
                            x = line.split(":", 1)
                            target = Target(x[0], x[1].strip().split(), None)
                        elif regexpcommand.match(line):
                            if lastintargetdep or lastincommand:
                                lastintargetdep = False
                                lastincommand = True
                                commands.append(line)
                            else:
                                # TODO : refactor with exception for invalid make file
                                print("Invalid make file 1")
                                sys.exit(1)
                        else:
                            # TODO : refactor with exception for invalid make file
                            print("Invalid make file 2")
                            sys.exit(1)
            if target:
                target.commands = commands
                targets.append(target)

        finally:
            file_object.close()
            return targets


def print_make_file(makefile):
    for target in makefile:
        line = target.value + " : " + target.dependencies_to_string()
        print(line)
        for command in target.commands:
            line = "\t" + command
            print(line)