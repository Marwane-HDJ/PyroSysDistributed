from os.path import abspath
import sys
import time
import Queue
import threading

import Pyro4

from DataStructure.targetTree import TargetTree

from Utilities.parser import parse
import worker


__author__ = 'marouane'


class Master(object):
    def __init__(self, tree=None):
        self.workers = []
        self.free_workers = Queue.Queue()
        self.job_results = Queue.Queue()
        self.tree = tree
        # queue of tasks to be done, the master should put the tasks here as they are available to run_job_dispatcher
        self.jobs_to_do = Queue.Queue()
        # for i in range(100):
        # self.jobs_to_do.put(i)

    def list_contents(self):
        return self.workers

    def register(self, worker_name):  # register the worker and send work to it
        self.workers.append(worker_name)
        self.free_workers.put(worker_name)
        print("worker " + worker_name + " registred.")

    def echo(self, message):
        print(message)
        return "Hi slave"

    def prepare_jobs(self):
        job_list = list
        job_list = self.tree.no_child_nodes()
        for job in job_list:
            self.jobs_to_do.put_nowait(job.value)

    def prepare_jobs_cut(self):
        job_list = list
        job_list = self.tree.no_child_nodes_cut()
        for job in job_list:
            self.jobs_to_do.put(job.value)

    def send_work(self, worker_name, job):
        worker = Pyro4.Proxy("PYRONAME:" + worker_name)
        # block until there is some work to do
        return worker.do_work(job)
        # print("The result is : " + result)


    def run_job_dispatcher(self):
        def dispatch_jobs():
            while True:
                print("We want you !")
                self.prepare_jobs()

                job = self.jobs_to_do.get(block=True)
                worker = self.free_workers.get(block=True)
                result = self.send_work(worker, job)
                self.receive_result(result)
                # print("work sent")
                # self.receive_result(result)
                # self.free_workers.put(worker)


        th_disp_jobs = threading.Thread(target=dispatch_jobs)
        th_disp_jobs.setDaemon(True)
        th_disp_jobs.start()

    def run_result_box(self):
        def receive_results():
            print("Job mail box start")
            while True:
                result = self.job_results.get(block=True)
                var = result.split(":")
                if len(var) == 4:
                    worker = var[1] + ":" + var[2]
                    command = var[3]
                    print("received : " + command + " from " + worker)
                    self.tree.node_satisfied(command)
                    self.prepare_jobs()
                    self.free_workers.put(worker, block=True)

        th_rcv_results = threading.Thread(target=receive_results)
        th_rcv_results.setDaemon(True)
        th_rcv_results.start()

    def receive_result(self, result):
        self.job_results.put(result)


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

    # daemon = Pyro4.Daemon()
    # master_uri = daemon.register(master)
    #ns = Pyro4.locateNS()
    #ns.register("master", master_uri)

    def test():
        Pyro4.Daemon.serveSimple(
            {
                master:"master"
            }, host=worker.get_ip_address('em1'),
            ns=True
        )
    testThread = threading.Thread(target=test)
    testThread.start()

    print("Master ready.")
    master.run_job_dispatcher()
    master.run_result_box()
    #daemon.requestLoop()
    testThread.join()


if __name__ == "__main__":
    main()
