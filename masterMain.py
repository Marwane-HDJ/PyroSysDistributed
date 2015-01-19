__author__ = 'monssef'

import Pyro4
import Queue
import threading
from DataStructure.targetTree import TargetNode
from DataStructure.targetTree import TargetTree
from worker import Worker
from os.path import abspath
import sys
from Utilities.parser import parse


class Master(object):
    def __init__(self):
        self.workers = []
        # queue of tasks to be done, the master should put the tasks here as they are available to run_job_dispatcher
        self.to_be_done = Queue.Queue()
        for i in range(100):
            self.to_be_done.put(i)

    def list_contents(self):
        return self.workers

    def register(self, worker_name=""):  # register the worker and send work to it
        self.workers.append(worker_name)
        print("worker " + worker_name + " registred.")
        self.send_work(worker_name)
        print("work sended")

    def send_work(self, worker_name):
        worker = Pyro4.Proxy("PYRONAME:" + worker_name)
        print(worker.worker_name)
        while True:  # send work forever
            nodeTask = self.to_be_done.get(block=True)
            result = (worker.do_work(nodeTask.value))  # block until there is some work to do
            if result:
                nodeTask.state = 3
                TargetNode.recursive_execute(nodeTask.parent, self.to_be_done)
            else:
                # TODO: raise exception or add the work again to the queue
                print("error")

def main():
    if 2 != len(sys.argv):
        print("Arguments incorrects")
        # TODO : refactor with exceptions
    else:
        f_path = abspath(sys.argv[1])
        makefile = parse(f_path)
        tree = TargetTree(makefile)
        master = Master()
        tree.recursive_execute(tree.tree_root, master.to_be_done)
        daemon=Pyro4.Daemon()
        ns=Pyro4.locateNS()
        uri=daemon.register(master)
        ns.register("master", uri)
        daemon.requestLoop()

if __name__ == "__main__":
    main()