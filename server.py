import socket
from _thread import *
import time
import re, pickle

send = 1
username = ''
host = '127.0.0.1'
port = 5555
port1 = 5556
acc_sockets = []
address = []
clients = [] * 200
clintsDict = {}
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((host, port))
    # s.bind((host, port1))
    s.setblocking(1)
except socket.error as e:
    print(str(e))

s.listen()
new = 0
remove = 0


def open_conn_thread(conn, addr):
    global remove, new, username, clintsDict, send
    if addr not in address:
        acc_sockets.append(conn)
        address.append(addr)
        new = 1
        remove = 0
    while True:
        try:
            send = 1
            serverData = conn.recv(4096)
            serverData = serverData.decode('utf-8')
            print(serverData)
            if 'initSecName' in serverData or 'groupchatInitx3' in serverData or 'PrvChtMem' in serverData:
                print('not sending')
                send = 0


        except ConnectionResetError as e:
            rmindex = acc_sockets.index(conn)
            acc_sockets.pop(rmindex)
            rmname = clients[rmindex]
            clients.pop(rmindex)
            for c in acc_sockets:
                try:
                    c.sendall(str.encode('\n\n** ' + rmname + ' left PowerPuff Chat for now :( **\n'))
                except:
                    pass
            break

        if not serverData:
            break

        if 'PrvChtMem' in serverData:
            send = 0
            # index = acc_sockets.index(conn)
            # print('person asked : ', conn)
            # cl = clients[index]
            # for c in clients:
            #     if c != cl:
            #         print('sending' , c)
            #         conn.sendall(str.encode(c))
            #         print('sending to : ', conn)
            #     print('sent')
            # conn.sendall(str.encode('overx3bajunca'))
            print('sending', clients)
            sendMem = pickle.dumps(clients)
            conn.sendall(sendMem)

        if new == 1 and 'initSecName:' in serverData:
            index = acc_sockets.index(conn)
            username = re.sub('initSecName:', '', serverData)
            clintsDict[username] = conn
            clients.insert(index, username)


        if new == 1 and 'groupchatInitx3' in serverData:
            userIndex = acc_sockets.index(conn)
            username = clients[userIndex]
            serverData = '\n** ' + username + ' joined the chat **\n'
            for c in acc_sockets:
                try:
                    c.sendall(str.encode(serverData))
                    new = 0
                    remove = 0
                    send = 0
                except:
                    pass

        if 'privatex3bajunca:' in serverData:
            privateTalk = serverData.replace('privatex3bajunca:', '')
            privateconn= clintsDict.get(privateTalk, 'Missing value')
            privateconn.sendall(str.encode('privateInitx3bajunca'))

        if send:
            try:
                serverData = clients[acc_sockets.index(conn)] + ': '+ serverData
                for c in acc_sockets:
                    if c != conn:
                        c.sendall(str.encode(serverData))
            except:
                pass

    conn.close()

while True:
    conn, addr = s.accept()
    print('connected to : ' , addr)
    start_new_thread(open_conn_thread,(conn,addr))

