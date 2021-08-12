from collections import deque
from concurrent.futures import Future
from threading import Thread,Lock

class Queuey:
    def __init__(self,max_size):
        self.mutext=Lock()
        self.max_size=max_size
        self.items =deque()
        self.getters=deque()
        self.putters=deque()

    def get_noblock(self):
        with self.mutext:
            if self.items:
                #wake some putter 
                if self.putters:
                    self.putters.popleft().set_result(True)
                return self.items.popleft(),None
            else :
                fut=Future()
                self.getters.append(fut)
                return None,fut

    def put_noblock(self,item):
        with self.mutext:
            if len(self.items) <self.max_size:
                self.items.append(item)
                #wake some getter
                if self.getters:
                    self.getters.popleft().set_result(self.items.popleft())
            else:
                fut=Future()
                self.putters.append(fut)
                return fut

    def get_sync(self):
        item,fut=self.get_noblock()
        if fut:
            item=fut.result()
        return item

    def put_sync(self,item):
        #try to put the item untill no future is return hence we succuflly put the item
        while True:
            fut=self.put_noblock(item)
            if fut is None:
                return
            fut.result()



