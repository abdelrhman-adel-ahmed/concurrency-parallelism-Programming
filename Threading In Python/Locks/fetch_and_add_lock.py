from threading import Lock, Thread, currentThread


class Fetch_and_add:
    def __init__(self) -> None:
        self.ticket = 0
        self.turn = 0

    # fetch and add is supported by the hardware ,its an atomic operation like xchg
    def fetch_and_add(self):
        old = self.ticket
        self.ticket += 1
        return old

    def acquire(self):
        my_turn = self.fetch_and_add()
        while self.turn != my_turn:
            continue

    def relase(self):
        self.turn += 1


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


lock = Fetch_and_add()
t1 = Thread(target=add_one, args=(lock,))
t2 = Thread(target=add_one, args=(lock,))
start = time.perf_counter()
t1.start()
t2.start()
t1.join()
t2.join()
end = time.perf_counter()
print(balance)
print(end - start)
