from collections import deque
import time
import heapq


class Sched():
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
                func()

class QueueClosed(Exception):
    pass

class Result:
    def __init__(self,value=None,exc=None):
        self.value=value
        self.exc=exc

    def result(self):
        if self.exc:
            raise self.exc
        else:
            return self.value

class AsyncQueue:
    def __init__(self):
        self.items=deque()
        self.waiting=deque() # all getters waiting for data
        self._closed=False   

    def close(self):
        self._closed=True
        if self.waiting :
            for func in self.waiting:
                s.call_soon(func)
                
    def put(self,item):
        if self._closed:
            raise QueueClosed()

        self.items.append(item)
        if self.waiting:
            func=self.waiting.popleft()
            s.call_soon(func)
            #func() #--> might get deep calls ,recursion

    def get(self,callback):
        #if item is avilabale we will call _cosume and send the item 
        if self.items:
            callback(Result(value=self.items.popleft()))  # still run if closed
        #if not we will put the get(_consume) in the waiting area 
        else:
            if self._closed:
                callback(Result(exc=QueueClosed()))
            self.waiting.append(lambda:self.get(callback))

s=Sched()

def producer(q,count):
    def _run(n):
        if n < count:
            print('producing',n)
            q.put(n)
            s.call_later(1,lambda:_run(n+1))
        else:
            print('producer done')
            #q.put(None)
            q.close() #no more item will been produced
    _run(0)

def consumer(q):
    def _consume(result):
        try:
            item =result.result()
            print('consume',item)
            s.call_later(2,lambda:consumer(q))
        except QueueClosed:
            print('consumer done')
    q.get(callback=_consume)

q=AsyncQueue()
s.call_soon(lambda:producer(q,5))
s.call_soon(lambda:consumer(q))
s.run()

