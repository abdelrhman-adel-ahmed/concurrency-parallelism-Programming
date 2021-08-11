import time
from collections import deque
import heapq    
from select import select
from socket import *

class Scheduler():
    def __init__(self):
        self.tasks=deque()
        self.sleeping=[]  
        self.sequence=0
        self._read_waiting = {}
        self._write_waiting ={}

    def call_later(self,delay,func):
        self.sequence+=1 
        deadline=time.time()+delay
        heapq.heappush(self.sleeping, (deadline,self.sequence,func))        


    def call_soon(self,func):
        self.tasks.append(func)


    def read_wait(self,fd,func):
        self._read_waiting[fd]=func

    def write_wait(self,fd,func):
        self._write_waiting[fd]=func

    def run(self):
        while any([self.tasks,self.sleeping,self._read_waiting,self._write_waiting]):
            if not self.tasks:
                if self.sleeping:
                    deadline,_,func=heapq.heappop(self.sleeping)
                    timeout=deadline-time.time()
                    if timeout < 0: #if the task already finish sleeping
                        timeout=0
                else :
                    timeout=None

                can_read,can_write,_=select(self._read_waiting,self._write_waiting,[],
                timeout)
                for fd in can_read:
                    self.tasks.append(self._read_waiting.pop(fd))

                for fd in can_write:
                    self.tasks.append(self._write_waiting.pop(fd))

                now =time.time()
                while self.sleeping:
                    if now > self.sleeping[0][0]:
                        print('enterd')
                        self.tasks.append(heapq.heappop(self.sleeping)[2])
                    else:
                        break
                self.tasks.append(func)

            while self.tasks:
                func=self.tasks.popleft()
                func() 

    def new_task(self,coro):
        self.tasks.append(Task(coro)) 

    async def sleep(self,delay):
        self.call_later(delay,self.current)
        self.current=None
        await switch()

    async def recv(self,socket,buffer_size):
        self.read_wait(socket,self.current)
        self.current=None #follow the sleep protocol 
        await switch()
        return socket.recv(buffer_size)

    async def send(self,socket,data):
        self.write_wait(socket,self.current)
        self.current=None
        await switch()
        return socket.send(data)

    async def accept(self,socket):
        self.read_wait(socket,self.current)
        self.current=None
        await switch()
        return socket.accept()

class Task:
    def __init__(self,coro):
        self.coro=coro #wrappe coro

    def __call__(self): #advance the coro when event loop call them 
        try:
            sched.current=self
            self.coro.send(None)
            if sched.current:
                sched.tasks.append(self)
        except  StopIteration:
            pass

class Queueclosed(Exception):
    pass

class AsyncQueue():
    def __init__(self):
        self.items=deque()
        self.waiting=deque()
        self._closed=False
    
    def close(self):
        self._closed=True
        if self.waiting:
            for func in self.waiting:
                sched.tasks.append(func)  # Reschedule waiting tasks
        del self.waiting
      
    async def put(self,item):
        if self._closed:
            raise Queueclosed()
            
        self.items.append(item)
        if self.waiting:
            sched.tasks.append(self.waiting.popleft()) # Reschedule waiting tasks

    async def get(self):
        while not self.items:
            if self._closed:
                raise Queueclosed()
            self.waiting.append(sched.current)
            sched.current=None
            await switch()
        return self.items.popleft()

        
class Awitable():
    def __await__(self):
        yield 

def switch():
    return Awitable()

#coro based functions
async def producer(q,count):
    for n in range(count):
        print("prodcuer",n)
        await q.put(n)
        await sched.sleep(1) 
    print('producer done')
    q.close()

async def consumer(q):
    while True:
        try:
            item=await q.get()
            print('consumer',item)
            await switch()
        except Queueclosed:
            break
    print('consumer done')

#call back based function
def countdown(n):
    if n>0:
        print('down',n)
        sched.call_later(4,lambda:countdown(n-1))

def countup(stop,x=0):
    if x < stop:
        print('up',x)
        sched.call_later(1,lambda:countup(stop,x+1))


async def server(address):
    sock=socket(AF_INET,SOCK_STREAM)
    sock.bind(address)
    sock.listen(1)
    while True:
        client ,add =await sched.accept(sock)
        print(f'{add} got connected')
        sched.new_task(echo_handler(client))

async def echo_handler(client):
    while True:
        data= await sched.recv(client,1000)
        if not data:
            break
        await sched.send(client,b'got '+ data)
    print('connection closed')



if __name__ == "__main__":
    sched=Scheduler()
    q=AsyncQueue()
    sched.new_task(producer(q,5))
    sched.new_task(consumer(q))

    sched.call_soon(lambda:countdown(5))
    sched.call_soon(lambda:countup(20))

    sched.new_task(server(("",25000)))

    sched.run()
