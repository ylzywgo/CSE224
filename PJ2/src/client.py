import argparse
import xmlrpc.client
import os
from os import listdir
from os.path import isfile, join

import hashlib

file_name = "index.txt"
local_FileInfoMap = {}
cur_FileInfoMap = {}
updated_FileInfoMap = {}

local_blockmap = {}

'compute hash list for one file'
def computeHashList(filename, block_size):
    hash_list = []
    with open(filename, 'rb') as f:
        while True:
            one_chunk = f.read(block_size)
            if not one_chunk:
                break  # done
            hash_value = hashlib.sha256(one_chunk).hexdigest()
            if hash_value not in local_blockmap:
                local_blockmap[hash_value] = one_chunk
            hash_list.append(hash_value)
    return hash_list

def printIndexFile(filepath):
    f = open(filepath, 'r')  # open index.txt
    print(f.read())
    f.close()

def getLocalFileInfoMap(filepath):
    with open(filepath, 'r') as f:
        line = f.readline()
        while line:  # handle index.txt line by line, note there isn't check on new created file
            if line == '' or line == ' ' or line == '\n':
                break
            cur_file = line.rstrip('\n')
            cur_file = cur_file.split(' ')
            cur_file = [ele for ele in cur_file if ele]  # delete empty string
            if len(cur_file) < 3 or cur_file[1] == '':
                # print("error index format")
                break
            cur_file_name = cur_file[0]
            cur_version = int(cur_file[1])
            local_FileInfoMap[cur_file_name] = [cur_version, cur_file[2:]]
            line = f.readline()
    return

' scan every file and compute hashlist for every file '
# save to cur_FileInfoMap
def computeBaseDirHashlist(basedir, block_size):
    local_f = listdir(basedir)
    local_file = []
    for file in local_f:
        if isfile(join(basedir, file)) and file != file_name:
            local_file.append(file)
    for file in local_file:
        hash_list = computeHashList(basedir + '/' + file, block_size)
        if file not in local_FileInfoMap: # new file
            fileInfo = [1, hash_list]
            cur_FileInfoMap[file] = fileInfo
        else:
            if local_FileInfoMap[file][1] != hash_list:  # updated file
                fileInfo = [local_FileInfoMap[file][0]+1, hash_list]
                cur_FileInfoMap[file] = fileInfo
            else:
                fileInfo = [local_FileInfoMap[file][0], hash_list]
                cur_FileInfoMap[file] = fileInfo
    return


def printFileInfoMap(fileInfoMap):
    s = ''
    for file in fileInfoMap:
        s = s + file + ' '
        fileinfo = fileInfoMap[file]
        if len(fileinfo) < 2:
            # print("index format error")
            return
        s = s + str(fileinfo[0]) + ' '
        for hash in fileinfo[1]:
            s = s + hash + ' '
        print(s)
        s = ''
    print('')
    return

def downloadFile(basedir, fileInfoMap, filename):
    file_blocks = fileInfoMap[file][1]
    filepath = basedir + '/' + filename
    if file_blocks[0] == '0':   # tombstone version, no need to create new file in local
        if os.path.exists(filepath):
            os.remove(filepath)
        return
    with open(filepath, 'wb+') as f:
        for hash in file_blocks:
            one_block = client.surfstore.getblock(hash)
            f.write(one_block.data)
    return

''' return 1: new created 2. updated 3. unchanged 4. deleted '''
def checkFileStatus(filename):
    if filename in cur_FileInfoMap and filename in local_FileInfoMap and local_FileInfoMap[filename][1] == ['0']:
        return 1
    if filename in cur_FileInfoMap:
        if filename in local_FileInfoMap:
            if not local_FileInfoMap[filename][1]:
                # print("file " + filename + ' new created')
                return 1
            elif local_FileInfoMap[filename][0] == cur_FileInfoMap[filename][0]:
                # print("file " + filename + ' unchanged')
                return 3
            else:
                # print("file " + filename + ' updated')
                return 2
        else:
            # print("file " + filename + ' new created')
            return 1
    else:   # not in current basedir but in previous base dir
        # print("file " + filename + ' deleted')
        return 4

def updateLocalFileInfoMap():
    with open(filepath, 'w+') as f:
        for file in updated_FileInfoMap:
            f.write(file)
            f.write(' ')
            f.write(str(updated_FileInfoMap[file][0]))
            f.write(' ')
            for i in range(0, len(updated_FileInfoMap[file][1])-1):
                f.write(updated_FileInfoMap[file][1][i])
                f.write(' ')
            f.write(updated_FileInfoMap[file][1][len(updated_FileInfoMap[file][1])-1])
            f.write('\n')
    return

# put blocks that don't exist in remote to remote
def putAllBlocks(filename, cur_FileInfoMap):
    sublist = client.surfstore.hasblocks(cur_FileInfoMap[filename][1])
    blocks_not_in_remote = [ele for ele in cur_FileInfoMap[filename][1] if ele not in sublist]
    for i in blocks_not_in_remote:
        if i != '0':
            client.surfstore.putblock(local_blockmap[i])
    return

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="SurfStore client")
    parser.add_argument('hostport', help='host:port of the server')
    parser.add_argument('basedir', help='The base directory')
    parser.add_argument('blocksize', type=int, help='Block size')
    args = parser.parse_args()

    try:
        updated_FileInfoMap = {}
        local_FileInfoMap = {}
        cur_FileInfoMap = {}

        server_port = "http://" + args.hostport
        client = xmlrpc.client.ServerProxy(server_port)
        # Test ping
        client.surfstore.ping()
        # print("Ping() successful")


        filepath = args.basedir + '/' + file_name
        if not os.path.exists(filepath):
            f = open(filepath, "w+")
            f.close()

        print("Initial Local Index Content")
        printIndexFile(filepath)
        getLocalFileInfoMap(filepath)

        'scan every file and compute hashlist for every file'
        computeBaseDirHashlist(args.basedir, args.blocksize)
        'update local index file with local files(updated, created, deleted)'
        print("Metadata")
        printFileInfoMap(cur_FileInfoMap)

        fileInfoMap = client.surfstore.getfileinfomap()
        print("Initial Remote Index Content")
        printFileInfoMap(fileInfoMap)


        '''
        new file::
        1. local new file1, not in remote    ---->  upload file1, remote ver =1, local ver = 1
        2. local new file1, remote tombstone  ----> upload file1, remote ver++; local ver = remote ver
        3. local new file1, remote has file1 already ---> return error; download file1; local ver = remote ver
        updated file:
        1. updated file1, remote ver > local ver(remote been changed by others) ---> error; download; local ver = remote ver
        2. updated file1, remote ver == local ver(no one changed it after last sync) ---> upload; remote ver++; local ver++
        unchanged file:
        1. remote ver > local ver(remote been changed by others) ---> download; local ver = remote ver
        2. remote ver == local ver ---> skip
        deleted file:
        1. remote ver == local ver   ----> remote hashlist set []; remote ver++; local ver++;
        2. remote ver > local ver    ----> error; download, local ver = remote ver
        '''
        all_files = set(local_FileInfoMap.keys()).union(set(cur_FileInfoMap.keys()))
        remoteExtraFile = list(set(fileInfoMap.keys()) - set(all_files))
        for file in remoteExtraFile:
            downloadFile(args.basedir, fileInfoMap, file)
            updated_FileInfoMap[file] = [fileInfoMap[file][0], fileInfoMap[file][1]]

        for file in all_files:
            status = checkFileStatus(file)
            # fileInfoMap = client.surfstore.getfileinfomap()
            if status == 1:   # new file
                if file not in fileInfoMap:
                    putAllBlocks(file, cur_FileInfoMap)
                    suc = client.surfstore.updatefile(file, cur_FileInfoMap[file][0], cur_FileInfoMap[file][1])
                    if suc:
                        updated_FileInfoMap[file] = [cur_FileInfoMap[file][0], cur_FileInfoMap[file][1]]
                    else:
                        fileInfoMap = client.surfstore.getfileinfomap()
                        downloadFile(args.basedir, fileInfoMap, file)
                        updated_FileInfoMap[file] = [fileInfoMap[file][0], fileInfoMap[file][1]]
                elif fileInfoMap[file][1] == ['0']:
                    putAllBlocks(file, cur_FileInfoMap)
                    suc = client.surfstore.updatefile(file, fileInfoMap[file][0]+1, cur_FileInfoMap[file][1])
                    if suc:
                        updated_FileInfoMap[file] = [fileInfoMap[file][0]+1, cur_FileInfoMap[file][1]]
                    else:
                        fileInfoMap = client.surfstore.getfileinfomap()
                        downloadFile(args.basedir, fileInfoMap, file)
                        updated_FileInfoMap[file] = [fileInfoMap[file][0], fileInfoMap[file][1]]
                else:
                    # print("error when uploading new files to remote")
                    downloadFile(args.basedir, fileInfoMap, file)
                    updated_FileInfoMap[file] = [fileInfoMap[file][0], fileInfoMap[file][1]]
            elif status == 2:   # updated
                if file not in fileInfoMap:
                    # print("error! The updated file should already be on remote")
                    continue
                elif fileInfoMap[file][0] > local_FileInfoMap[file][0]:
                    # print("error when uploading updated files to remote")
                    downloadFile(args.basedir, fileInfoMap, file)
                    updated_FileInfoMap[file] = [fileInfoMap[file][0], fileInfoMap[file][1]]
                else:
                    putAllBlocks(file, cur_FileInfoMap)
                    suc = client.surfstore.updatefile(file, fileInfoMap[file][0] + 1, cur_FileInfoMap[file][1])
                    if suc:
                        updated_FileInfoMap[file] = [fileInfoMap[file][0]+1, cur_FileInfoMap[file][1]]
                    else:
                        fileInfoMap = client.surfstore.getfileinfomap()
                        downloadFile(args.basedir, fileInfoMap, file)
                        updated_FileInfoMap[file] = [fileInfoMap[file][0], fileInfoMap[file][1]]

            elif status == 3:    # unchanged
                if file not in fileInfoMap:
                    # print("error! The unchanged file should already be on remote")
                    continue
                elif fileInfoMap[file][0] > local_FileInfoMap[file][0]:
                    downloadFile(args.basedir, fileInfoMap, file)
                    updated_FileInfoMap[file] = [fileInfoMap[file][0], fileInfoMap[file][1]]
                else:   # ??? not sure if get fileInfoMap here
                    updated_FileInfoMap[file] = [fileInfoMap[file][0], cur_FileInfoMap[file][1]]

            else:   # deleted
                if file not in fileInfoMap:
                    # print("error! The deleted file should already be on remote")
                    continue
                elif fileInfoMap[file][0] > local_FileInfoMap[file][0]:
                    # print("error when uploading updated (delete) files to remote")
                    downloadFile(args.basedir, fileInfoMap, file)
                    updated_FileInfoMap[file] = [fileInfoMap[file][0], fileInfoMap[file][1]]
                else:
                    if local_FileInfoMap[file][1] == ['0']:
                        updated_FileInfoMap[file] = [local_FileInfoMap[file][0], local_FileInfoMap[file][1]]
                        continue
                    else:
                        suc = client.surfstore.updatefile(file, fileInfoMap[file][0] + 1, ['0'])
                        if suc:
                            updated_FileInfoMap[file] = [fileInfoMap[file][0] + 1, ['0']]
                        else:
                            fileInfoMap = client.surfstore.getfileinfomap()
                            downloadFile(args.basedir, fileInfoMap, file)
                            updated_FileInfoMap[file] = [fileInfoMap[file][0], fileInfoMap[file][1]]


        print("New Remote Index")
        fileInfoMap = client.surfstore.getfileinfomap()
        printFileInfoMap(fileInfoMap)

        print("New Local Index")
        updateLocalFileInfoMap()
        printIndexFile(filepath)

    except Exception as e:
        print("Client: " + str(e))

