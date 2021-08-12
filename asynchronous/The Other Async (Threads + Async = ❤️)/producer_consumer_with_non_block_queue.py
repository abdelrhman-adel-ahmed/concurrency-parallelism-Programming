from queuy import *

def producer(q,n):
    for i in range(n):
        q.put_sync(i)
    q.put_sync(None)

def consumer(q):
    while True:
        item=q.get_sync()
        if item is None:
            break
        print(item)


q=Queuey(2)
Thread(target=producer,args=(q,10)).start()
Thread(target=consumer,args=(q,)).start()

