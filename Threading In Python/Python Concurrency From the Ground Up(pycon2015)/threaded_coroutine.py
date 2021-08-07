from socket  import *
from t1 import fib
from collections import deque
from queue import Queue
from select import select
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor



tasks=deque()

recv_wait={} #mapping socket to tasks (generators)
send_wait={}
future_wait={}
pool=ThreadPoolExecutor()
future_notify,future_event=socketpair()

"""
the problem is we launch thread to calc the fib ,but if we call the result it will block 
so the solution is to put yield but that will block all the programme because the select 
work for fb, so when it yield we put the future in the future_wait and we add the done
call back and then programme procced ,because the add_done_callback is the last thing in the 
elif block so we will go back to our loop,we also add the future_monitor to the task first
thing so its  waiting for recieving on future_event socket, and when the result is present and 
thread is finished it will append the future to the tasks queue again so we when we call
next on it we now can collect the result and it will not block because the result is present
now
"""
def future_done(future):
    tasks.append(future_wait.pop(future))
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
            #while no active tasks to run then we wait for i/o(on socket)'
            #and then when it ready it return the socket that is ready 
            #so now we have to put it back to the tasks to call next on it and get to to procced 
            can_rec,can_send,_ = select(recv_wait,send_wait,[])
            for t in can_rec:
                tasks.append(recv_wait.pop(t))
            for t in can_send:
                tasks.append(send_wait.pop(t))

        task=tasks.popleft()
        try:
            why ,what =next(task)
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
