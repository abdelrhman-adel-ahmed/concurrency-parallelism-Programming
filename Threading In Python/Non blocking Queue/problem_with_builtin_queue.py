from queue import Queue
from threading import Lock, Thread, currentThread
from time import sleep

# one way to break the built in Queue join function :is to make the put method sleep for while that way the unfinished_tasks will be 0
# and when task_done get called it will notify the join
q = Queue()


def producer():
    for i in range(10):
        q.put(i)
        print(f"producer {i}")
        sleep(1)
    q.put(None)


def consumer():
    while True:
        item = q.get()
        if item == None:
            q.task_done()
            break
        q.task_done()
        print(f"consumer {item}")


t1 = Thread(target=producer)
t2 = Thread(target=consumer)
t1.start()
t2.start()
q.join()
print(12)
