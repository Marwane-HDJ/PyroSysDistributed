__author__ = 'marouane'

import Pyro4


class Master(object):
    def __init__(self):
        self.workers = []

    def list_contents(self):
        return self.workers

    def register(self, worker):
        self.workers.append(worker)
        print("worker {0} registred.".format(worker))


def main():
    master = Master()
    Pyro4.Daemon.serveSimple(
        {
            master: "master"
        },
        ns=True)


if __name__ == "__main__":
    main()

