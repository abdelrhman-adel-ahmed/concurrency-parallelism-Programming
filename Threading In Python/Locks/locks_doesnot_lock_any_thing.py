

"""
A primitive lock is in one of two states, "locked" or "unlocked". It is created in the 
unlocked state. It has two basic methods, acquire() and release(). When the state is unlocked,
acquire() changes the state to locked and returns immediately. When the state is locked, acquire() 
blocks until a call to release() in another thread changes it to unlocked, then the acquire()
call resets it to locked and returns. The release() method should only be called in the locked 
state; it changes the state to unlocked and returns immediately. If an attempt is made to release
an unlocked lock, a RuntimeError will be raised.
note 1 :if thread call acquired and then it acquired the lock if it call acquired again before realse
it will block because the second acquired is waiting for the state to be unlocked  
note 2 :acquire has defult bool args that either make it block or not and a timeout for how time
it will wait for the lock , and return true if it acquired and false if not in case its specified 
to be not blocking 
"""
from threading import Lock ,Thread ,enumerate,main_thread
import time  

lock = Lock()
  
num = 1
  
def sumOne():
    global num

    s=lock.acquire()
    print("sum one acquire the lock",s)
    time.sleep(1) # make it sleep so the other thread go and run ,and bypass the lock
    num = num + 1

    try:
        lock.release()
        print("not realsed 1")
    except:
        pass
  
def sumTwo():
    global num

    s=lock.acquire(0)
    print("sum two bypass acquire the lock",s)
    num = num / 2

    lock.release()
    print('sum two relased the lock') 
    #it can realse it neverless its not the one that aquire it ,not like rlock which only can be released by the thread that acquire it 
    #so when sumone thread continue it will throw an error when it try to relase the lock   

  
# calling the functions
Thread(target=sumOne).start()
Thread(target=sumTwo).start()

main_thread=main_thread()

for thread in enumerate():
    if thread !=main_thread:
        thread.join()
  
# displaying the value of shared resource
print(num)
