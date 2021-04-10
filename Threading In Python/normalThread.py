#sum the numbers from 1 to 1000000

import time
from threading import *

a = 0


def first_half(lock):
    global a
    for i in range(500000):
        lock.acquire()
        a += i
        lock.release()


def second_half(lock):
    global a
    for i in range(500000, 1000001):
        lock.acquire()
        a += i
        lock.release()


lock = Lock()
t1 = Thread(target=first_half, args=[lock])
t2 = Thread(target=second_half, args=[lock])

t1.start()
t2.start()
t1.join()
t2.join()
print(a)
