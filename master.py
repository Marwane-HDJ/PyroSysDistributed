import time

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

    def register(self, worker_name):  # register the worker and send work to it
        self.workers.append(worker_name)
        print("worker " + worker_name + " registred.")

    def echo(self, message):
        print message
        return "Hi slave"

    def send_work(self, worker_name):
        worker = Pyro4.Proxy("PYRONAME:" + worker_name)
        # print (" sending work")
        result = (worker.do_work(self.to_be_done.get(block=True)))  # block until there is some work to do
            # Do something with the result

    def run(self):
        def dispatch_jobs():
            while True:
                time.sleep(3)
                if len(self.workers) == 0:
                    print("no workers")
                else:
                    self.send_work(self.workers[0])

        thread = threading.Thread(target=dispatch_jobs)
        thread.setDaemon(True)
        thread.start()


def main():
    master = Master()
    daemon = Pyro4.Daemon()
    master_uri = daemon.register(master)
    ns = Pyro4.locateNS()
    ns.register("master", master_uri)
    print "Master ready."
    master.run()
    daemon.requestLoop()


if __name__ == "__main__":
    main()

