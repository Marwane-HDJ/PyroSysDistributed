__author__ = 'monssef'

import Pyro4
import threading
import time


class Worker(object):
    def __init__(self, name):
        self.name = name

    def do_work(self, command_files):
        print (command_files)
        time.sleep(1)
        return True

def main():
    worker = Worker("worker1")
    daemon=Pyro4.Daemon()
    ns=Pyro4.locateNS()
    uri=daemon.register(worker)
    ns.register(worker.name, uri)
    # register itself at the master and it will send work automatically
    master = Pyro4.Proxy("PYRONAME:master")
    master.register(worker.name)
    daemon.requestLoop()

if __name__ == "__main__":
    main()
