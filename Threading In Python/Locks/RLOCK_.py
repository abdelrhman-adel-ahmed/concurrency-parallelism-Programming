
"""
1-normally you cannot acquire normal lock more than once 
2-A Lock object can be released by any thread.	
3-rlock is the opposite of that ,but they are slower 
"""
import threading
import time

class X:
    def __init__(self):
        self.a = 1
        self.b = 2
        self.lock = threading.RLock()

    def changeA(self):
        with self.lock:
            self.a = self.a + 1

    def changeB(self):
        with self.lock:
            self.b = self.b + self.a

    def changeAandB(self):
        # you can use chanceA and changeB thread-safe!
        with self.lock:
            self.changeA() # a usual lock would block at here
            self.changeB()
        print(f'{threading.current_thread()} a={self.a} b={self.b}')

obj=X()

threading.Thread(target=obj.changeAandB).start()
threading.Thread(target=obj.changeAandB).start()
