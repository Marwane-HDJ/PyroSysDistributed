from os.path import abspath
import socket
import struct
import sys
import Queue
import threading
import fcntl
from time import sleep

import Pyro4

from DataStructure.targetTree import TargetTree
from Utilities.parser import parse, parse_v2
from filesContainer import FilesContainer


__author__ = 'marouane'

Pyro4.config.REQUIRE_EXPOSE = True


@Pyro4.expose
class Master(object):
    def __init__(self, tree=None, target=""):
        self.workers = []
        self.free_workers = Queue.Queue()
        self.job_results = Queue.Queue()
        self.tree = tree
        self.fc = None
        if self.tree and len(target) > 0:
            self.tree.change_tree_root(target)
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

    @staticmethod
    def echo(message):
        print(message)
        return "Hi slave"

    def prepare_jobs(self):
        job_list = list
        job_list = self.tree.no_child_nodes()
        for job in job_list:
            if job.exist:
                for f in job.file_dependencies:
                    try:
                        self.fc.store(f.value)
                    except:
                        print("File not found " + f.value)
                self.jobs_to_do.put(job.value)

    @staticmethod
    def send_work(worker_name, job):
        worker = Pyro4.Proxy("PYRONAME:" + worker_name)
        worker.do_work(job)

    def run_job_dispatcher(self):
        def dispatch_jobs():
            while True:
                print("We want you !")
                self.prepare_jobs()
                sleep(3)
                job = self.jobs_to_do.get(block=True)
                worker = self.free_workers.get(block=True)
                self.send_work(worker, job)
                # self.receive_result(result)
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
                if len(var) == 5:
                    worker = var[1] + ":" + var[2] + ":" + var[3]
                    command = var[4]
                    print("received : " + command + " from " + worker)
                    self.tree.node_satisfied(command)
                    self.prepare_jobs()
                    self.free_workers.put(worker, block=True)

        th_rcv_results = threading.Thread(target=receive_results)
        th_rcv_results.setDaemon(True)
        th_rcv_results.start()

    def receive_result(self, result):
        self.job_results.put(result)


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


def main():
    tree = None
    makefile = None
    master = None
    interface = "eth0"

    if 2 == len(sys.argv):
        # if the argument is the makefile name
        f_path = abspath(sys.argv[1])
        makefile = parse_v2(f_path)
        tree = TargetTree(makefile)
        master = Master(tree=tree)
    elif 3 == len(sys.argv):
        f_path = abspath(sys.argv[1])
        makefile = parse_v2(f_path)
        tree = TargetTree(makefile)
        target = sys.argv[2]
        master = Master(tree=tree, target=target)
    elif 4 == len(sys.argv):
        f_path = abspath(sys.argv[1])
        makefile = parse_v2(f_path)
        tree = TargetTree(makefile)
        target = sys.argv[2]
        master = Master(tree=tree, target=target)
        interface = sys.argv[3]
    else:
        master = Master()

    host_ip = get_ip_address(interface)
    daemon = Pyro4.Daemon(host=host_ip)
    ns = Pyro4.locateNS(host=host_ip)
    master_uri = daemon.register(master)
    ns.register("master", master_uri)
    print("Master register in naming server done")
    tree.nodes_ns_register(daemon, ns)
    print("Nodes register in naming server done")
    master.fc = FilesContainer()
    fc_uri = daemon.register(master.fc)
    ns.register("FilesContainer", fc_uri)

    # def test():
    # Pyro4.Daemon.serveSimple(
    # {
    # master: "master"
    # }, host=get_ip_address('eth0'),
    # ns=True
    # )
    #
    # testThread = threading.Thread(target=test)
    # testThread.start()

    master.run_job_dispatcher()
    master.run_result_box()
    print("Master ready")
    daemon.requestLoop()

    # testThread.join()


if __name__ == "__main__":
    main()
