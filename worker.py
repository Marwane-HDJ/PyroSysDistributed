import os
import random
import time
import socket
import fcntl
import struct

import Pyro4
import threading
import sys
from subprocess import call
import subprocess

__author__ = 'marouane'

Pyro4.config.REQUIRE_EXPOSE = True


@Pyro4.expose
class Worker(object):
    def __init__(self, name, daemon=None, ns=None, fc=None):
        self.name = name
        self.master = None
        self.daemon = daemon
        self.ns = ns
        self.fc = fc

    def register(self, master):
        print("Worker {0} want to register.".format(self.name))
        master.register(self.name)
        print("Worker {0} registred".format(self.name))

    def look_for_file(self, file):
        content = self.fc.take(file)
        with open(file, 'w') as f:
            f.write(content)
        print("file written")

    def post_file(self, file):
        self.fc.store(file)

    def execute_command(self, command):
        if len(command) != 0:
            #os.system(command)
            p = subprocess.Popen(command, shell=True)
            p.communicate()

    def do_work(self, job):
        print(self.name + ":" + str(job))
        node = Pyro4.Proxy("PYRONAME:" + job)
        v = node.get_value()
        print("found : " + v)
        for dep in node.get_file_dependencies():
            print("need : " + dep.get_value())
            self.look_for_file(dep.get_value())

        self.execute_command(node.get_command()[0])

        self.post_file(v)

        self.master.receive_result("result:" + self.name + ":" + job)


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


def main():
    print("Work begin")

    interface = "wlan0"

    if 2 == len(sys.argv):
        interface = sys.argv[1]

    host_ip = get_ip_address(interface)
    worker = Worker('worker:' + host_ip + ":" + str(random.random()))

    daemon = Pyro4.Daemon(host="localhost")
    ns = Pyro4.locateNS(host="localhost")
    worker.daemon = daemon
    worker.ns = ns
    worker_uri = daemon.register(worker)
    ns.register(worker.name, worker_uri)

    # def test():
    # Pyro4.Daemon.serveSimple(
    # {
    # worker: worker.name,
    # }, host=host_ip,
    # ns=True
    # )
    #
    # testThread = threading.Thread(target=test)
    # testThread.start()

    print("Worker registering in the master server")
    worker.master = Pyro4.Proxy("PYRONAME:master")
    worker.master.register(worker.name)

    print("Worker looking for file container")
    worker.fc = Pyro4.Proxy("PYRONAME:FilesContainer")

    print("Worker ready.")
    daemon.requestLoop()

    # testThread.join()


if __name__ == "__main__":
    main()
