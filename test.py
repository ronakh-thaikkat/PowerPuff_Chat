import threading
import time
import threading
from time import sleep
import pickle

import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 5555))
s.sendall(str.encode('heheh'))
data = s.recv(4096)
arr = pickle.loads(data)
print(arr)




