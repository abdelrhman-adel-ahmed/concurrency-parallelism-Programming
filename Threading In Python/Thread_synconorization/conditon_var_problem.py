import time
from threading import Condition, Lock, Thread

cv = Condition()
done = 0 #state var


def thread1():
    global done
    with cv:
        print("the notifer is runnnning")
        time.sleep(2)
        done = 1
        cv.notify()
    print("notifer finishhhh and notify all other waiting threads (i hope so)")


def thread2():
    global done
    # spining waste
    while done == 0:
        with cv:
            print("oh shit iam about to call wait and hope the notifer didnot finish yet")
            cv.wait()
            print("yaaah i get notifed finally")


"""
note:that here we check for the state var first and then try to grap the lock.
the problem if we dont have a lock is the notify function can be called first before
wait and then it return because no waiting are here ,and then now we retrurn from the 
spining lock (acquire block and spin untill the state in unlock) and wait get called and it blocked
for ever ,same happen here even we have a lock because the first thread execute first 
and its having the lock so the other thread couldnot aquire it and call wait and then when the 
first thread call notify no waiting threads are there so it do nothing and reutrn and then 
the second thread come and call wait and its blocked for ever ,one solution is to start the 
second thread fist that way it will take the lock call wait that will cause to the lock to be
realsed and then the first thread start call notify that cause the lock to be realsed and then 
the waiting thread unblocked and acquire the lock and continue exection from the waiting 
function
OR THAT T1 IS NOT SLEEP AND IMMIDEALTY SET THE DONE TO 1 THEN NOTIFY OF COURES NO THREAD ARE
WAITING BUT T2 WHEN IT CHECKES FOR THE DONE VAR IT ALERDY 1 SO IT CONTINUE WITHOUT WAITING 
"""

t1 = Thread(target=thread1)
t1.start()

t2 = Thread(target=thread2)
t2.start()


