from socket  import *
import time

socket=socket(AF_INET,SOCK_STREAM)
socket.connect(('localhost',25000))

#if we run it twice due to the gil the time it take to perfome will increase because now we switch between fib_handle thread to handle multiple clients
while True:
    start=time.time()
    socket.send(b'30')
    resp=socket.recv(1000)
    end=time.time()
    print(end-start)
