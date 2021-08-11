import time
from collections import deque
import heapq    


class Schedulr:

    def __init__(self):
        self.ready=deque()
        self.sleeping=[]
        self.sequence=0
        self.current=None

    async def sleep(self,delay):
        deadline=time.time()+delay
        self.sequence+=1
        heapq.heappush(self.sleeping,(deadline,self.sequence,self.current))
        self.current=None
        await switch()

    def add_task(self,coro):
        self.ready.append(coro)
    
    def run(self):
        while self.ready or self.sleeping:
            if not self.ready:
                deadline,_,coro=heapq.heappop(self.sleeping)
                delta=deadline -time.time()
                if delta > 0 :
                    time.sleep(delta)
                self.ready.append(coro)
            self.current=self.ready.popleft()
            try:
                self.current.send(None)
                if self.current:
                    self.ready.append(self.current)
            except StopIteration:
                pass

sched=Schedulr()

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
                sched.ready.append(func)
        del self.waiting
      
    async def put(self,item):
        if self._closed:
            raise Queueclosed()
            
        self.items.append(item)
        if self.waiting:
            sched.ready.append(self.waiting.popleft())

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
"""
await switch is kindaa our yield statment so we send untill we hit await 
if it regular get or put then if it gonna block then await switch got called 
to stop and re enter the run loop again 
"""
def switch():
    return Awitable()

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

q=AsyncQueue()
sched.add_task(producer(q,5))
sched.add_task(consumer(q))
sched.run()
