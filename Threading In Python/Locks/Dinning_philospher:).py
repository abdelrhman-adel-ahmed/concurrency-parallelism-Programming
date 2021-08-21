import random
import time
from concurrent.futures import ThreadPoolExecutor
from threading import Lock, Thread, current_thread

sticks = [Lock() for _ in range(5)]

# we put sleep to simulate blocking operation ,so the other thread will enter


def philospher(n):
    time.sleep(random.random())
    with sticks[n]:
        print(f"{current_thread()} ,thread {n} is equired first lock {n}")
        time.sleep(random.random())
        with sticks[(n + 1) % 5]:
            print(f"{current_thread()} ,thread {n} is equired second lock {(n+1)%5}")
            print("eating", n)
            time.sleep(random.random())
        print(f"{current_thread()} ,thread {n} is realse second lock {(n+1)%5}")
    print(f"{current_thread()} ,thread {n} is realse first lock {n}")


pool = ThreadPoolExecutor()

phils = [Thread(target=philospher, args=(n,)) for n in range(5)]
# phils2 = [pool.submit(philospher, n) for n in range(5)]
for p in phils:
    p.start()
