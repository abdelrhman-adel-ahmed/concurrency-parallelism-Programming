from socket  import *
from t1 import fib
from threading import Thread
import sys

print(sys.getswitchinterval())
#sys.setswitchinterval(.000005) # new 3.2 every .05 sec it switch
#sys.setcheckinterval(1) old python 2.7 before Antoine Pitrou 3.2

def fib_server(address):
    server=socket(AF_INET,SOCK_STREAM)
    server.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    server.bind(address)
    server.listen(5)
    while True:
        client,add=server.accept()
        print(f"connection {add}")
        Thread(target=fib_handler,args=(client,add)).start()

def fib_handler(client,addr):
    while True:
        try:
            req=client.recv(100)
            num=int(req)
            result=fib(num)
            result=str(result).encode('ascii')+b'\n'
            client.send(result)
        except ConnectionResetError:
            break
    print(f'connection closed {addr}')

fib_server(('',25000))
