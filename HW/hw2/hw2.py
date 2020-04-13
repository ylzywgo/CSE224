import xmlrpc.client

s = xmlrpc.client.ServerProxy("http://cse224.sysnet.ucsd.edu:7777/RPC2")
print(s.litserver.getLiterature("A53280596"))