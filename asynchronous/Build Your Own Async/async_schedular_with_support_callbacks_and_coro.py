import time
from collections import deque
import heapq    




class Scheduler():
    def __init__(self):
        self.tasks=deque()
        self.sleeping=[]  
        self.sequence=0

    def call_later(self,delay,func):
        self.sequence+=1 
        deadline=time.time()+delay
        heapq.heappush(self.sleeping, (deadline,self.sequence,func))        


    def call_soon(self,func):
        self.tasks.append(func)

    def run(self):
        while self.tasks or self.sleeping:
            if not self.tasks and self.sleeping:
                #find nearest deadline
                deadline,_,func=heapq.heappop(self.sleeping)
                delta=deadline-time.time()
                if delta > 0:
                    time.sleep(delta)
                self.tasks.append(func)

            while self.tasks:
                func=self.tasks.popleft()
                func() #--> if it coro it will call the __call__ (we make it callable to
                #solve this problem,to have both regular functions(callbacks) and coro)

    def new_task(self,coro):
        self.tasks.append(Task(coro)) # --> make the coro callable

    async def sleep(self,delay):
        self.call_later(delay,self.current)
        self.current=None
        await switch()



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
                sched.tasks.append(func)
        del self.waiting
      
    async def put(self,item):
        if self._closed:
            raise Queueclosed()
            
        self.items.append(item)
        if self.waiting:
            sched.tasks.append(self.waiting.popleft())

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


if __name__ == "__main__":
    sched=Scheduler()
    q=AsyncQueue()
    sched.new_task(producer(q,5))
    sched.new_task(consumer(q))

    sched.call_soon(lambda:countdown(5))
    sched.call_soon(lambda:countup(20))
    sched.run()
