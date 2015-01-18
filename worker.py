__author__ = 'marouane'
import Pyro4
import threading
import time


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


def main():
    print("1")
    worker = Worker("worker1")


    # Use another thread to register itself
    t1 = threading.Thread(target=worker.register_at_nameserver)
    t1.start()
    print("Passed here ")

    # register itself at the master and it will send work automatically
    master = Pyro4.Proxy("PYRONAME:master")
    master.register(worker.name)
    t1.join()


if __name__ == "__main__":
    main()

