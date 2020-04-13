from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from socketserver import ThreadingMixIn
from hashlib import sha256
import argparse
from threading import Timer
import random
import xmlrpc.client

# 720 1200 300

EleTimeStart = 750
EleTimeEnd = 1500
HEARTBEAT = 300

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

class threadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

class Node:
    def __init__(self, id):
        self.id = id
        self.state = 0  # follower: 0, candidate: 1, leader: 2
        self.term = 0
        self.voteFor = None
        self.votes = 0
        self.timer = None
        self.crash = 0

        self.log_entry = list()
        self.lastLogIndex = -1
        self.commitIndex = -1
        self.fileinfomap = dict()

# A simple ping, returns true
def ping():
    """A simple ping method"""
    print("Ping()")
    return True

# Retrieves the server's FileInfoMap
def getfileinfomap():
    """Gets the fileinfo map"""
    if cur.crash:
        raise ("This node is crashed. Try another one")
    if cur.state != 2:
        raise ("This node is not a leader. Try another one")
    cur.log_entry.append((cur.term, "getfileinfomap"))
    cur.lastLogIndex += 1
    curIndexHere = cur.lastLogIndex
    while cur.commitIndex < curIndexHere:
        if cur.crash == 1:
            raise ("This node is crashed. Try another one")
        if cur.state != 2:
            raise ("This node is not a leader. Try another one")
        continue
    return cur.fileinfomap

# Update a file's fileinfo entry
def updatefile(filename, version, hashlist):
    """Updates a file's fileinfo entry"""
    if cur.crash == 1:
        raise ("This node is crashed. Try another one")
    if cur.state != 2:
        raise ("This node is not a leader. Try another one")
    # entry = "updatefile|" + filename + "|" + str(version) +"|" + str(hashlist)
    cur.log_entry.append((cur.term, "updatefile"))
    cur.lastLogIndex += 1
    curIndexHere = cur.lastLogIndex
    while cur.commitIndex < curIndexHere:
        if cur.crash == 1:
            raise ("This node is crashed. Try another one")
        if cur.state != 2:
            raise ("This node is not a leader. Try another one")
        continue
    if filename not in cur.fileinfomap or cur.fileinfomap[filename][0] <= version:
        cur.fileinfomap[filename] = [version, hashlist]

    return True

def updatefilelocal(filename, version, hashlist):
    """Updates a file's fileinfo entry"""
    if cur.crash == 1:
        raise ("This node is crashed. Try another one")
    if filename not in cur.fileinfomap or cur.fileinfomap[filename][0] <= version:
        cur.fileinfomap[filename] = [version, hashlist]
    return True

# PROJECT 3 APIs below

# Queries whether this metadata store is a leader
# Note that this call should work even when the server is "crashed"
def isLeader():
    """Is this metadata store a leader?"""
    return not cur.crash and cur.state == 2

# "Crashes" this metadata store
# Until Restore() is called, the server should reply to all RPCs
# with an error (unless indicated otherwise), and shouldn't send
# RPCs to other servers
def crash():
    """Crashes this metadata store"""
    cur.crash = 1
    if cur.timer:
        cur.timer.cancel()
    return True

# "Restores" this metadata store, allowing it to start responding
# to and sending RPCs to other nodes
def restore():
    """Restores this metadata store"""
    cur.crash = 0
    if cur.state == 2:
        setAsLeader()
    else:
        setEleTimer()
    return True

def generateEleTime():
    return random.randint(EleTimeStart, EleTimeEnd) * 1.0 / 1000

def setEleTimer():
    if cur.timer:
        cur.timer.cancel()
    time = generateEleTime()
    cur.timer = Timer(time, setAsCandidiate)
    cur.timer.start()


# "IsCrashed" returns the status of this metadata node (crashed or not)
# This method should always work, even when the node is crashed
def isCrashed():
    """Returns whether this node is crashed or not"""
    return cur.crash

def requestVoteForAll():
        for hostport in serverlist:
            try:
                client = xmlrpc.client.ServerProxy('http://' + hostport)

                if len(cur.log_entry) == 0:
                    lastLogTerm = -1
                else:
                    lastLogTerm = cur.log_entry[cur.lastLogIndex][0]

                term, vote = client.surfstore.requestVote(cur.id, cur.term, lastLogTerm, cur.lastLogIndex)
                if term > cur.term:
                    setAsFollower()
                    cur.term = term
                    return
                elif vote:
                    cur.votes += 1
                # dealing with index prefer
                else:
                    # if cur term == voter term and cur lastLogIndex < voter lastLogIndex
                    continue
            except Exception:
                pass
        if cur.votes > (len(serverlist) + 1) // 2:
            setAsLeader()

# Requests vote from this server to become the leader
def requestVote(serverid, term, lastLogTerm, lastLogIndex):
    """Requests vote to be the leader"""
    if isCrashed():
        return term, False

    curLastLogTerm = -1
    if cur.lastLogIndex != -1:
        curLastLogTerm = cur.log_entry[cur.lastLogIndex][0]

    if cur.term < term:
        if curLastLogTerm < lastLogTerm or (curLastLogTerm == lastLogTerm and cur.lastLogIndex <= lastLogIndex):
            '''
            local server votes to serverid
            change local to follower
            reset the timer
            '''
            cur.term = term
            cur.voteFor = serverid
            cur.state = 0  # follower
            cur.votes = 0
            # not sure whether the timer need to be reset
            setEleTimer()
            return cur.term, True
        else:
            cur.term = term
            return cur.term, False
    elif cur.term > term:
        '''
        if local is a follower and its term is larger than all other candidates at this time
        it will refuse to vote for all of them 
        until some higher term shows up or its timer gone
        '''
        return cur.term, False
    # cur.term == term compare their index
    else:
        if cur.lastLogIndex <= lastLogIndex:
            if cur.voteFor == None:
                cur.voteFor = serverid
                cur.term = term
                return cur.term, True
            else:
                return cur.term, False
        else:
            cur.term = term
            return cur.term, False


def setAsLeader():
    if cur.timer:
        cur.timer.cancel()
    cur.state = 2
    cur.voteFor = None
    cur.votes = 0
    cur.timer = Timer(HEARTBEAT*1.0/1000, appendAllEntries)
    cur.timer.start()
    

def setAsFollower():
    cur.state = 0
    setEleTimer()
    cur.voteFor = None
    cur.votes = 0

def setAsCandidiate():
    cur.state = 1
    cur.term += 1
    cur.votes = 1
    cur.voteFor = cur.id
    setEleTimer()
    requestVoteForAll()

def appendAllEntries():
    '''
    send heartbeat to all servers
    '''
    # count how many follower append successfully
    count = 0
    commitIndex = cur.lastLogIndex
    for hostport in serverlist:
        try:
            client = xmlrpc.client.ServerProxy('http://' + hostport)
            '''
            need to consider if current term is updated
            '''
            term, success = client.surfstore.appendEntries(cur.term, cur.fileinfomap, cur.log_entry, cur.lastLogIndex, cur.commitIndex)
            # if hit follower with higher term, change it to follower
            if term > cur.term:
                cur.term = term
                setAsFollower()
                return
            elif success:
                count += 1
        except Exception:
            pass
    if count >= (len(serverlist) + 1) // 2:
        # change index
        cur.commitIndex = commitIndex
    if cur.timer:
        cur.timer.cancel()
    cur.timer = Timer(HEARTBEAT*1.0/1000, appendAllEntries)
    cur.timer.start()

# Updates fileinfomap
def appendEntries(term, fileinfomap, log_entry, lastLogIndex, commitIndex):
    """Updates fileinfomap to match that of the leader"""
    '''need to consider the state of the cur node'''
    if isCrashed():
        return term, False
    if cur.term > term:  # change the requesting candidate to follower
        return cur.term, False
    else:
        setAsFollower()
        cur.term = term
        cur.lastLogIndex = lastLogIndex
        cur.log_entry = log_entry
        cur.fileinfomap = fileinfomap
        if cur.commitIndex < commitIndex:
            # for i in range(cur.commitIndex + 1, commitIndex + 1):
            #     func = cur.log_entry[i].split("|")
            #     if len(func) > 1:
            #         updatefilelocal(func[1], (int)(func[2]), func[3])
            cur.commitIndex = commitIndex
        return cur.term, True

def tester_getversion(filename):
    if filename in cur.fileinfomap:
        return cur.fileinfomap[filename][0]
    else:
        return 0

# Reads the config file and return host, port and store list of other servers
def readconfig(config, servernum):
    """Reads cofig file"""
    fd = open(config, 'r')
    l = fd.readline()

    maxnum = int(l.strip().split(' ')[1])

    if servernum >= maxnum or servernum < 0:
        raise Exception('Server number out of range.')

    d = fd.read()
    d = d.splitlines()

    for i in range(len(d)):
        hostport = d[i].strip().split(' ')[1]
        if i == servernum:
            host = hostport.split(':')[0]
            port = int(hostport.split(':')[1])

        else:
            serverlist.append(hostport)


    return maxnum, host, port


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="SurfStore server")
        parser.add_argument('config', help='path to config file')
        parser.add_argument('servernum', type=int, help='server number')

        args = parser.parse_args()

        config = args.config
        servernum = args.servernum

        # server list has list of other servers
        serverlist = []

        # maxnum is maximum number of servers
        maxnum, host, port = readconfig(config, servernum)

        #hashmap = dict()

        print("Attempting to start XML-RPC Server...")
        print(host, port)
        server = threadedXMLRPCServer((host, port), requestHandler=RequestHandler)
        server.register_introspection_functions()
        server.register_function(getfileinfomap,"surfstore.getfileinfomap")
        server.register_function(updatefile,"surfstore.updatefile")
        # Project 3 APIs
        server.register_function(isLeader,"surfstore.isLeader")
        server.register_function(crash,"surfstore.crash")
        server.register_function(restore,"surfstore.restore")
        server.register_function(isCrashed,"surfstore.isCrashed")
        server.register_function(requestVote,"surfstore.requestVote")
        server.register_function(appendEntries,"surfstore.appendEntries")
        server.register_function(tester_getversion,"surfstore.tester_getversion")
        print("Started successfully.")
        print("Accepting requests. (Halt program to stop.)")

        cur = Node(servernum)
        setEleTimer()

        server.serve_forever()

    except Exception as e:
        print("Server: " + str(e))
