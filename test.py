import threading
import time
import threading
from time import sleep
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 5555))
s.sendall(str.encode('Initial Hello'))
def this_thing():
    while True:
        try:
            data = s.recv(4096)
            print(data.decode('utf-8'))
        except Exception as e:
            pass

def that_thing():
    for i in range(10000):
        sleep(0.5)
        s.sendall(str.encode('Hello'))
        print('happening2')

threading.Thread(target=this_thing, args=[]).start()
threading.Thread(target=that_thing, args=[]).start()



