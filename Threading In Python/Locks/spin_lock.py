from threading import Thread, currentThread


class Spin_lock:
    def __init__(self) -> None:
        self.lock = 0

    def xchg(self):
        old = self.lock
        self.lock = 1
        return old

    def acquire(self):
        while self.xchg() == 1:
            continue

    def relase(self):
        self.lock = 0


balance = 0

import time


def add_one(lock):
    global balance
    for i in range(10):
        lock.acquire()
        iner = balance
        iner += 1
        time.sleep(0.0001)
        balance = iner
        lock.relase()


lock = Spin_lock()
t1 = Thread(target=add_one, args=(lock,))
t2 = Thread(target=add_one, args=(lock,))
t1.start()
t2.start()
t1.join()
t2.join()
print(balance)
