from socket  import *
import time
from threading import Thread


socket=socket(AF_INET,SOCK_STREAM)
socket.connect(('localhost',25000))

# req per sec, if we run perf1 while running this the gil by design periotize the cpu tasks
#and our prog here is just i/o because it send very short req of fib 1 which get calculted 
#very fast so it basically i/o so we will so tremendous drop of req/sec
#os is opposite to that it gives priority to short running tasks os it doesnot starve 
n=0

def monitor():
    global n 
    while True:
        time.sleep(1)
        print(n,'req/sec')
        n=0
Thread(target=monitor).start()

while True:
    socket.send(b'1')
    resp=socket.recv(100)
    n+=1
