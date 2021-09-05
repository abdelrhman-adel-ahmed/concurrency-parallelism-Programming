import time
from threading import Condition, Lock, Thread


cv = Condition()
done = 0  


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
    # the cheking is done after we acquire the lock so if notify get call before wait
    # we still gonna able to run because the done is already =1 so we will not going to call
    # the wait
    with cv:
        while done == 0:
            print("oh shit iam about to call wait and hope the notifer didnot finish yet")
            cv.wait()
        print("yaaah i get notifed finally")


t1 = Thread(target=thread1)
t1.start()

t2 = Thread(target=thread2)
t2.start()
