from collections import deque
from queue import Queue
from threading import Condition, Lock, Thread, current_thread
from time import sleep

"""
my implementation is diffrent from the built it class , mainly on how we join the queue ,here you only need to call the task done once 
"""
class queue:
    def __init__(self, max_size: int = 0) -> None:
        self.max_size = max_size
        self.queue = deque()

        self.mutex = Lock()
        self.not_full = Condition(self.mutex)
        self.not_empty = Condition(self.mutex)
        self.not_finished = Condition(self.mutex)
        self.done = 0

    def size(self):
        return len(self.queue)

    def put(self, item):
        with self.not_full:
            # if we have max_size
            if self.max_size > 0:
                while self.size() >= self.max_size:
                    print(f"{current_thread()} producer wait")
                    self.not_full.wait()
            self.queue.append(item)
            print(f"item appeded {item}")
            self.not_empty.notify()

    def get(self):
        with self.not_empty:
            while self.size() == 0:
                print(f"{current_thread()} consumer wait")
                self.not_empty.wait()
            item = self.queue.pop()
            self.not_full.notify()
            return item

    def task_done(self):
        with self.not_finished:
            if self.done == 1:
                raise ValueError("task_done called more than once")
            self.done = 1
            self.not_finished.notify()

    def join(self):
        with self.not_finished:
            while self.done == 0:
                self.not_finished.wait()


q = queue(1)


def producer():
    for i in range(10):
        q.put(i)
    q.put(None)
  
   


def consumer():
    while True:
        item = q.get()
        if item == None:
            q.task_done()
            print(f"{current_thread()} got {item}")
            break
        print(f"{current_thread()} got {item}")


t1 = Thread(target=producer)
t1.start()
li = []
for i in range(3):
    t = Thread(target=consumer)
    # solution to make all of them exit is to make them daemon or put sentenail value for each
    # consumer,but this will not work here because we call task_done inside the none block
    # "try to put three None in the queue when you end"
    t.daemon = True
    t.start()
    li.append(t)


q.join()

print(12)
