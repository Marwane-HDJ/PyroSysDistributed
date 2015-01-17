# saved as client.py
import Pyro4

#demonstration of  use: client
filesContainer=Pyro4.Proxy("PYRONAME:example.filesContainer")    # use name server object lookup uri shortcut
print filesContainer.take("make1.txt")