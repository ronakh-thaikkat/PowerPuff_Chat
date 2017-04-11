import socket
from _thread import *
import time
import re, pickle

username = ''
host = '127.0.0.1'
port = 5555
acc_sockets = []
clients = [] * 200
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((host, port))
    s.setblocking(1)
except socket.error as e:
    print(str(e))

s.listen()
new = 0
remove = 0


def open_conn_thread(conn, addr):
    # conn.sendall(str.encode('this is test'))
    print(clients)
    global remove, new, username
    if addr not in clients:
        acc_sockets.append(conn)
        new = 1
        remove = 0
    while True:
        try:
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
            print(clients)
            if len(clients) == 0:
                conn.sendall(str.encode('None of your friends are online now, sorry :('))
                conn.sendall(str.encode('overx3bajunca'))
            else:
                for c in clients:
                    conn.sendall(str.encode(c))
                conn.sendall(str.encode('overx3bajunca'))

        if new == 1 and 'initSecName:' in data:
            index = acc_sockets.index(conn)
            username = re.sub('initSecName:', '', data)
            clients.insert(index, username)
            remove = 1

        if new == 1 and remove == 1:
            for c in acc_sockets:
                c.sendall(str.encode('\n\n** ' + username + ' joined the chat **\n'))
                new = 0
                remove = 0
        else:
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

