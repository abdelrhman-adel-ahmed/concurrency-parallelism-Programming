
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
