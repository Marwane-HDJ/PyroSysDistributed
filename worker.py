import time
import socket
import fcntl
import struct

import Pyro4
import threading

__author__ = 'marouane'


class Worker(object):
    def __init__(self, name):
        self.name = name

    def register(self, master):
        print("Worker {0} want to register.".format(self.name))
        master.register(self.name)
        print("Worker {0} registred".format(self.name))

    def do_work(self, command_files):
        print(self.name + ":" + str(command_files))

        # return "I'm ready to work more, my master" + self.name
        return "result:" + self.name + ":" + command_files


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


def main():
    print("1")

    host_ip = get_ip_address("eth0")
    worker = Worker('worker:' + host_ip)


    def test():
        Pyro4.Daemon.serveSimple(
            {
                worker: worker.name,
            }, host=host_ip,
            ns=True
        )

    testThread = threading.Thread(target=test)
    testThread.start()

    print("Worker ready.")

    master = Pyro4.Proxy("PYRONAME:master")
    master.register(worker.name)

    print ("Done")
    testThread.join()


if __name__ == "__main__":
    main()
