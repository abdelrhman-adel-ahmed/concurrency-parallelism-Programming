import time
from threading import Thread

#acquire and release overheads added by the GIL while doing cpu bound tasks will increase the time more than one threaded programme !! :(.
#even if we use py 3.2 or higher version which removed the concept of ticks and add the concept of gil_drop_request


COUNT = 50000000


def countdown(n):
    while n > 0:
        n -= 1


start = time.time()
countdown(COUNT)
end = time.time()

print("Time taken in seconds -", end - start)


#--------------------------------------------------------------------------------
COUNT = 50000000

def countdown(n):
    while n > 0:
        n -= 1


t1 = Thread(target=countdown, args=(COUNT // 2,))
t2 = Thread(target=countdown, args=(COUNT // 2,))

start = time.time()
t1.start()
t2.start()
t1.join()
t2.join()
end = time.time()
print("Time taken in seconds -", end - start)
