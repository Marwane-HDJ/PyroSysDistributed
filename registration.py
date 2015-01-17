__author__ = 'marouane'

import sys
import Pyro4
import Pyro4.util

from worker import Worker

sys.excepthook = Pyro4.util.excepthook

master = Pyro4.Proxy("PYRONAME:master")
worker1 = Worker("1")
worker1.register(master)