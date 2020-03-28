import Network.netStream as ns
import time

nsc = ns.NetStream(0)
nsc.connect("127.0.0.1", 8888)
nsc.start()
time.sleep(4)
nsc.sendData("yes!")
str = nsc.getRecvData()
print str
nsc.close()