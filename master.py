from DataStructure.targetNode import TargetNode
from os.path import abspath
import sys
from DataStructure.targetTree import TargetTree
from Utilities.parser import parse

import cPickle as pickle
import time
import Pyro4
import Queue
import threading


__author__ = 'marouane'


class Master(object):
    def __init__(self, tree=None):
        self.workers = []
        self.free_workers = Queue.Queue()
        self.job_results = Queue.Queue()
        self.tree = tree
        # queue of tasks to be done, the master should put the tasks here as they are available to run_job_dispatcher
        self.to_be_done = Queue.Queue()
        for i in range(100):
            self.to_be_done.put(i)

    def list_contents(self):
        return self.workers

    def register(self, worker_name):  # register the worker and send work to it
        self.workers.append(worker_name)
        self.free_workers.put_nowait(worker_name)
        print("worker " + worker_name + " registred.")

    def echo(self, message):
        print(message)
        return "Hi slave"

    def send_work(self, worker_name):
        worker = Pyro4.Proxy("PYRONAME:" + worker_name)
        # block until there is some work to do
        result = worker.do_work(self.to_be_done.get(block=True))
        # print("The result is : " + result)
        self.receive_result(result)
        self.free_workers.put(worker_name)

    def receive_result(self, result):
        print("received : " + result)
        self.job_results.put(result)
        # TODO : change time for perf
        time.sleep(1)

    def run_job_dispatcher(self):
        def dispatch_jobs():
            while True:
                print("We want you !")
                self.send_work(self.free_workers.get(block=True))
                print("work sent")


        th_disp_jobs = threading.Thread(target=dispatch_jobs)
        th_disp_jobs.setDaemon(True)
        th_disp_jobs.start()

    def run_result_box(self):
        def receive_results():
            print("Job mail box start")
            while True:
                self.receive_result(self.job_results.get(block=True))

        th_rcv_results = threading.Thread(target=receive_results)
        th_rcv_results.setDaemon(True)
        th_rcv_results.start()


def main():
    tree = None
    makefile = None
    master = None

    if 2 == len(sys.argv):
        # if the argument is the makefile name
        f_path = abspath(sys.argv[1])
        makefile = parse(f_path)
        tree = TargetTree(makefile)
        master = Master(tree)
    else:
        master = Master()

    daemon = Pyro4.Daemon()
    master_uri = daemon.register(master)
    ns = Pyro4.locateNS()
    ns.register("master", master_uri)
    print("Master ready.")
    master.run_job_dispatcher()
    master.run_result_box()
    daemon.requestLoop()


if __name__ == "__main__":
    main()

