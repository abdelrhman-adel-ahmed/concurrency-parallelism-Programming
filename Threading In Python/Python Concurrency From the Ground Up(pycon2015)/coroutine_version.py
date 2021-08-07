from socket  import *
from t1 import fib
from collections import deque
from select import select

"""
when you run perf2 and then run long running calulation the req/sec drop to 0 because
we only have on thread so that thread when the long running cal will come it will stay
running untill it finish ,so we can solve that by hand the cpu work to another thread or 
process
"""
tasks=deque()
recv_wait={} #mapping socket to tasks (generators)
send_wait={}

def fib_server(address):
    server=socket(AF_INET,SOCK_STREAM)
    server.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    server.bind(address)
    server.listen(5)
    while True:
        yield 'recv',server
        client,add=server.accept()
        print(f"connection {add}")
        tasks.append(fib_handler(client,add))

def fib_handler(client,addr):
    while True:
        try:
            yield 'recv',client
            req=client.recv(100)
            num=int(req)
            result=fib(num)
            result=str(result).encode('ascii')+b'\n'
            yield 'send',client
            client.send(result)
        except ConnectionResetError:
            break
    print(f'connection closed {addr}')

def run():
    #as long as any tasks any where 
    while any([tasks,recv_wait,send_wait]):
        while not tasks:
            #while no active tasks to run then we wait for i/o
            can_rec,can_send,_ = select(recv_wait,send_wait,[])
            for t in can_rec:
                tasks.append(recv_wait.pop(t))
            for t in can_send:
                tasks.append(send_wait.pop(t))

        task=tasks.popleft()
        try:
            why ,what =next(task)
            #server always get puted in the recv wait dict ,client can either be 
            #in recv wait or send wait
            if why == 'recv':
                #must go wait somewhere 
                recv_wait[what]=task
            elif why == 'send':
                send_wait[what]=task
        except  StopIteration:
            print(f"task done")


tasks.append(fib_server(('',25000)))
run()
