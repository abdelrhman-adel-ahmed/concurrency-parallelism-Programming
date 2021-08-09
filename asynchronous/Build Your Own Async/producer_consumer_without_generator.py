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

class AsyncQueue:
    def __init__(self):
        self.items=deque()
        self.waiting=deque() # all getters waiting for data
        self._closed=False   

    def close(self):
        self._closed=True

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
            callback(self.items.popleft())  # still run if closed
        #if not we will put the get(_consume) in the waiting area 
        else:
            if self._closed:
                callback('None')
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

# def producer(q,count,n=0):
#     if n < count:
#         print('produce',n)
#         q.put(n)
#         s.call_later(3,lambda:producer(q,count,n+1))
#     else :
#         print('producer done')
#         q.put(None)

def consumer(q):
    def _consume(item):
        if item == 'None':  # queue closed check
           print("consumer done")
        else:
            print('consume',item)
            s.call_soon(lambda:consumer(q))
    q.get(callback=_consume)

q=AsyncQueue()
s.call_soon(lambda:producer(q,1))
s.call_soon(lambda:consumer(q))
s.run()
# if q.waiting:
#     func=q.waiting.popleft()
#     s.call_soon(func)
# s.run()

"""
                   the problem of message after close()
when we call_soon on producer the consumer will get the closing message on this setup 
if we call call_later on the producer what happend is :
1- we call_soon first time to put the producer in the tasks sched
2- call_soon first time put the consumer in the tasks sched 
3- run take the fist taks (producer) call it hit the _run(0) it 
 1- call the put method to put the item in the queue 
 2- return and then call the call_later to put the producer on the waiting 
 3- now the only task we have in the tasks queue is the consumer 
4- run then get the consumer and run it it q.get get called and we have item so we call 
the call back wich is the _consume function with the item as and arg 
so _consume get called and then it call_soon on consumer now only task in ready is this task
and remember we sill have producer on the waiting
5-run run again and we have task in ready queue which is consumer we call it go to get 
we dont have any item avilable so it go to the waiting area of the asyncqueue
6-run run again now we dont have any tasks in the tasks ready so we go to the waiting 
pull the producer run it now we finish so we print that we done and call the close 
7- run func come again there is no waiting or ready tasks
** despite we have the consumer on the async queue waiting but we never enter the put method 
to pull it out thats why it doesnot print (consumer done)

*hack is doing this at the end of the code:
if q.waiting:
    func=q.waiting.popleft()
    s.call_soon(func)
s.run()
*or create result class
"""
