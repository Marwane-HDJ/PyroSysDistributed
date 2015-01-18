__author__ = 'marouane'
import Pyro4
import threading
import time
import multiprocessing


class Worker(object):
    def __init__(self, name):
        self.name = name

    def register(self, master):
        print("Worker {0} want to register.".format(self.name))
        master.register(self.name)
        print("Worker {0} registred".format(self.name))

    def do_work(self, command_files):
        print (self.name + ":" + str(command_files))
        time.sleep(1)
        # return the resulting files
        return "I'm ready to work more, my master" + self.name

    def register_at_nameserver(self):
        print ("registering worker at NameServer")
        Pyro4.Daemon.serveSimple(
            {
                self: self.name
            }, host="localhost",
            ns=True)


def main():
    workerList = []
    for i in range(multiprocessing.cpu_count()):
        workerList.append(Worker(str(i)))

    for worker in workerList:
        print (worker.name)

    threadsList = []
    for worker in workerList:
        t1 = threading.Thread(target=worker.register_at_nameserver)
        t1.start()
        threadsList.append(t1)

    # Use another thread to register itself

    print("Passed here ")

    # register itself at the master and it will send work automatically

    for worker in workerList:
        master = Pyro4.Proxy("PYRONAME:master")
        t1 = threading.Thread(target=master.register, args =worker.name)
        t1.start()
        print ("worker started")
        threadsList.append(t1)

    for thread in threadsList:
        thread.join()


if __name__ == "__main__":
    main()

