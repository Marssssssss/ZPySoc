import Network.netStream as ns
import time

nsc = ns.NetStream(0)
nsc.connect("127.0.0.1", 8888)
nsc.start()
nsc.sendData("$help help create")
time.sleep(4)
str = nsc.getRecvData()
print str
time.sleep(3)
nsc.close()