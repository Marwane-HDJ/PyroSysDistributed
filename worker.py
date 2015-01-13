__author__ = 'marouane'


class Worker(object):
    def __init__(self, name):
        self.name = name


    def register(self, master):
        print("Worker {0} want to register.".format(self.name))
        master.register(self.name)
        print("Worker {0} registred".format(self.name))

