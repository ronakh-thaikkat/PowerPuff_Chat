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
            data = conn.recv(4096)
            data = data.decode('utf-8')
        except ConnectionResetError as e:
            rmindex = acc_sockets.index(conn)
            acc_sockets.pop(rmindex)
            rmname = clients[rmindex]
            clients.pop(rmindex)
            for c in acc_sockets:
                c.sendall(str.encode('\n\n** ' + rmname + ' left PowerPuff Chat for now :( **\n'))
            break

        if not data:
            break

        if 'PrvChtMem' in data:
            send = 0
            if len(clients) <= 1:
                conn.sendall(str.encode('None of your friends are online now, sorry :(\n'))
                conn.sendall(str.encode('overx3bajunca'))
            else:
                index = acc_sockets.index(conn)
                cl = clients[index]
                for c in clients:
                    if c != cl:
                        conn.sendall(str.encode(c))
                conn.sendall(str.encode('overx3bajunca'))

        if new == 1 and 'initSecName:' in data:
            index = acc_sockets.index(conn)
            username = re.sub('initSecName:', '', data)
            clintsDict[username] = conn
            clients.insert(index, username)
            remove = 1
            send = 0

        if new == 1 and remove == 1:
            data = '\n** ' + username + ' joined the chat **\n'
            for c in acc_sockets:
                try:
                    c.sendall(str.encode(data))
                    new = 0
                    remove = 0
                except:
                    pass

        if 'privatex3bajunca:' in data:
            privateTalk = data.replace('privatex3bajunca:', '')
            privateconn= clintsDict.get(privateTalk, 'Missing value')
            privateconn.sendall(str.encode('privateInitx3bajunca'))

        if send:
            try:
                data = clients[acc_sockets.index(conn)] + ': '+ data
                for c in acc_sockets:
                    c.sendall(str.encode(data))
            except:
                pass

    conn.close()

while True:
    conn, addr = s.accept()
    print('connected to : ' , addr)
    start_new_thread(open_conn_thread,(conn,addr))

