import socket
from _thread import *
import time
import re, pickle

send = 1
username = ''
host = '127.0.0.1'
port = 5555
acc_sockets = []
address = []
clients = [] * 200
clintsDict = {}
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((host, port))
    # s.bind((host, port1))
except socket.error as e:
    print(str(e))

s.listen()
new = 0
remove = 0
data_array = [1,2,3,4,5,7,7,6,4,5]
import pickle

def open_conn_thread(conn, addr):
    global remove, new, username, clintsDict, send
    if addr not in address:
        acc_sockets.append(conn)
        address.append(addr)
        while True:
           try:
               data = conn.recv(4096)
               print(data.decode('utf-8'))
               data_string = pickle.dumps(data_array)
               print(data_string)
               conn.sendall(data_string)
               print('sent')
           except:
               pass


    conn.close()

while True:
    conn, addr = s.accept()
    print('connected to : ' , addr)
    start_new_thread(open_conn_thread,(conn,addr))

