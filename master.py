__author__ = 'marouane'

import Pyro4
import Queue
import threading


class Master(object):
    def __init__(self):
        self.workers = []
        # queue of tasks to be done, the master should put the tasks here as they are available to run
        self.to_be_done = Queue.Queue()
        for i in range(100):
            self.to_be_done.put(i)

    def list_contents(self):
        return self.workers

    def register(self, worker_name=""):  # register the worker and send work to it
        self.workers.append(worker_name)
        print("worker " + worker_name + " registred.")
        self.send_work(worker_name)

    def echo(self, message):
        print message
        return "Hi slave"

    def send_work(self, worker_name):
        worker = Pyro4.Proxy("PYRONAME:" + worker_name)
        while True:  # send work forever
            # print (" sending work")
            result = (worker.do_work(self.to_be_done.get(block=True)))  # block until there is some work to do
            # Do something with the result


def main():
    master = Master()
    Pyro4.Daemon.serveSimple(
        {
            master: "master"
        }, host="localhost",
        ns=True)
    print "Ready."


if __name__ == "__main__":
    main()

