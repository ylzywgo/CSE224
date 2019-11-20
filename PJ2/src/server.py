from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from socketserver import ThreadingMixIn
import hashlib

FileInfoMap = {} ## remote index
blockMap = {}

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

class threadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

# A simple ping, returns true
def ping():
    """A simple ping method"""
    print("Ping()")
    return True

# Gets a block, given a specific hash value
def getblock(h):
    """Gets a block"""
    print("get block")
    if h in blockMap:
        print("has block returned")
        return blockMap[h]
    else:
        print("cannot find block")
        return ''

# Puts a block
def putblock(b):
    """Puts a block"""
    print("PutBlock()")
    b = b.data
    h = hashlib.sha256(b).hexdigest()
    blockMap[h] = b
    return True

# Given a list of hashes, return the subset that are on this server
def hasblocks(blocklist):
    """Determines which blocks are on this server"""
    print("HasBlocks()")
    sublist = []
    for hash in blocklist:
        if hash in blockMap:
            sublist.append(hash)
    return sublist

# Retrieves the server's FileInfoMap
'''
Returns a map of the files stored in the SurfStore cloud service. 
The keys in the map are filenames (as strings), and the values are FileInfo structures,
 which are tuples that have the file’s version as the first element of the tuple, 
 and a hash list as the second element of the tuple. Hash lists are represented as a list of strings.
'''
def getfileinfomap():
    """Gets the fileinfo map"""
    print("GetFileInfoMap()")
    return FileInfoMap

# Update a file's fileinfo entry
'''
Updates the FileInfo values associated with a file stored in the cloud. This method replaces the hash list for 
the file with the provided hash list only if the new version number is exactly one greater than the current version number. 
Otherwise, an error is sent to the client telling them that the version they are trying to store is not right (likely too old).

To create a file that has never existed, use the update_file() API call with a version number set to 1. 
To create a file that was previously deleted, update the version number that is one larger than the “tombstone” record.
'''
def updatefile(filename, version, blocklist):
    """Updates a file's fileinfo entry"""
    print("UpdateFile()")
    if version == 1 and filename in FileInfoMap:
        return False
    elif version == 1 and filename not in FileInfoMap:
        file1info = [version, blocklist]
        FileInfoMap[filename] = file1info
        return True
    if version != FileInfoMap[filename][0]+1:
        return False
    file1info = [version, blocklist]
    FileInfoMap[filename] = file1info
    return True

# PROJECT 3 APIs below

# Queries whether this metadata store is a leader
# Note that this call should work even when the server is "crashed"
def isLeader():
    """Is this metadata store a leader?"""
    print("IsLeader()")
    return True

# "Crashes" this metadata store
# Until Restore() is called, the server should reply to all RPCs
# with an error (unless indicated otherwise), and shouldn't send
# RPCs to other servers
def crash():
    """Crashes this metadata store"""
    print("Crash()")
    return True

# "Restores" this metadata store, allowing it to start responding
# to and sending RPCs to other nodes
def restore():
    """Restores this metadata store"""
    print("Restore()")
    return True


# "IsCrashed" returns the status of this metadata node (crashed or not)
# This method should always work, even when the node is crashed
def isCrashed():
    """Returns whether this node is crashed or not"""
    print("IsCrashed()")
    return True

if __name__ == "__main__":
    try:
        print("Attempting to start XML-RPC Server...")
        server = threadedXMLRPCServer(('localhost', 8080), requestHandler=RequestHandler)
        server.register_introspection_functions()
        server.register_function(ping,"surfstore.ping")
        server.register_function(getblock,"surfstore.getblock")
        server.register_function(putblock,"surfstore.putblock")
        server.register_function(hasblocks,"surfstore.hasblocks")
        server.register_function(getfileinfomap,"surfstore.getfileinfomap")
        server.register_function(updatefile,"surfstore.updatefile")

        server.register_function(isLeader,"surfstore.isleader")
        server.register_function(crash,"surfstore.crash")
        server.register_function(restore,"surfstore.restore")
        server.register_function(isCrashed,"surfstore.iscrashed")
        print("Started successfully.")
        print("Accepting requests. (Halt program to stop.)")
        server.serve_forever()
    except Exception as e:
        print("Server: " + str(e))
