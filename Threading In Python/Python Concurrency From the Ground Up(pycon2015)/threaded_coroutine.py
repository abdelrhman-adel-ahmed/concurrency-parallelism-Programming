from socket  import *
from t1 import fib
from collections import deque
from select import select
from concurrent.futures import ThreadPoolExecutor



tasks=deque()
recv_wait={} #mapping socket to tasks (generators)
send_wait={}
future_wait={}
pool=ThreadPoolExecutor()
future_notify,future_event=socketpair()

def future_done(future):
    tasks.append(future_wait[future])
    future_notify.send(b'x')

def future_monitor():
    while True:
        yield 'recv' ,future_event
        future_event.recv(100)

tasks.append(future_monitor())

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
            fut=pool.submit(fib,num)
            yield 'future_result', fut
            result = fut.result()
            #result=fut.result() #block so we still have the same problem
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
            #while no active tasks to run then we wait for i/o(om socket)
            can_rec,can_send,_ = select(recv_wait,send_wait,[])
            for t in can_rec:
                tasks.append(recv_wait.pop(t))
            for t in can_send:
                tasks.append(send_wait.pop(t))

        task=tasks.popleft()
        try:
            why ,what =next(task)
            #we mainly have four tasks server task,client task,future task,future_event task
            #server always get puted in the recv wait dict ,client can either be 
            #in recv wait or send wait
            if why == 'recv':
                #must go wait somewhere 
                recv_wait[what]=task
            elif why == 'send':
                send_wait[what]=task
            elif why =="future_result":
                future_wait[what]=task
                what.add_done_callback(future_done)
        except  StopIteration:
            print(f"task done")


tasks.append(fib_server(('',25000)))
run()
