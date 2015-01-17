# saved as fileSender.py
__author__ = 'monssef'

import Pyro4

#demonstration of use: server
from filesContainer import FilesContainer

files_container=FilesContainer()
files_container.store("make1.txt")

daemon=Pyro4.Daemon()                 # make a Pyro daemon
ns=Pyro4.locateNS()                   # find the name server
uri=daemon.register(files_container)      # register the greeting object as a Pyro object
ns.register("example.filesContainer", uri)  # register the object with a name in the name server

print "Ready."
daemon.requestLoop()                  # start the event loop of the server to wait for calls