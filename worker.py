__author__ = 'marouane'

import Pyro4
import threading
import time
import socket
import fcntl
import struct


class Worker(object):
    def __init__(self, name):
        self.name = name

    def register(self, master):
        print("Worker {0} want to register.".format(self.name))
        master.register(self.name)
        print("Worker {0} registred".format(self.name))

    def do_work(self, command_files):
        print (command_files)
        time.sleep(1)
        # return the resulting files
        return "I'm ready to work more, my master"


    def register_at_nameserver(self):
        print ("registering worker at NameServer")
        Pyro4.Daemon.serveSimple(
            {
                self: self.name
            }, host="localhost",
            ns=True)

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


def main():
    print("1")
    worker = Worker('worker'+":" + get_ip_address('eth0'))

    daemon = Pyro4.Daemon()
    worker_uri = daemon.register(worker)
    ns = Pyro4.locateNS()
    ns.register(worker.name, worker_uri)
    print "Worker ready."

    # register itself at the master and it will send work automatically
    master = Pyro4.Proxy("PYRONAME:master")
    master.register(worker.name)
    daemon.requestLoop()


if __name__ == "__main__":
    main()

