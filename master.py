__author__ = 'marouane'

import Pyro4
import Queue
import threading



class Master(object):
    def __init__(self):
        self.workers = []
        self.workerName = ""
        #queue of tasks to be done, the master should put the tasks here as they are available to run
        self.toBeDone = Queue.Queue()
        for i in range(100):
            self.toBeDone.put(i)

    def list_contents(self):
        return self.workers

    def register(self, workerName): #register the worker and send work to it
        self.workers.append(workerName)
        print("worker " + workerName + " registred.")
        self.sendWork(workerName)

    def echo(self,message):
        print message
        return "Hi slave"

    def sendWork(self, workerName):
        worker=Pyro4.Proxy("PYRONAME:" + workerName)
        while True: #send work forever
            #print (" sending work")
            result = (worker.doWork(self.toBeDone.get(block=True))) #block until there is some work to do
            #Do something with the result

def main():
    master = Master()
    Pyro4.Daemon.serveSimple(
        {
            master: "master"
        }, host="localhost",
        ns=True)
    print "Ready."




if __name__ == "__main__":
    main()

