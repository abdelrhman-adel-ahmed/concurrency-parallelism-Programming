# ------------------------------------------------------------
    #full credited to David Beazley ,
    #i only modify the code little bit and add comment to explain
    #programme steps
# ------------------------------------------------------------

# ------------------------------------------------------------
#                       === Tasks ===
# ------------------------------------------------------------
class Task(object):
    taskid = 0

    def __init__(self, target):
        Task.taskid += 1
        self.tid = Task.taskid  # Task ID
        self.target = target  # Target coroutine
        self.sendval = None  # Value to send

    # Run a task until it hits the next yield statement
    def run(self):
        return self.target.send(self.sendval)


# ------------------------------------------------------------
#                      === Scheduler ===
# ------------------------------------------------------------
from queue import Queue


class Scheduler(object):
    def __init__(self):
        self.ready = Queue()
        self.taskmap = {}

        # Tasks waiting for other tasks to exit
        self.exit_waiting = {}

    def new(self, target):
        newtask = Task(target)
        self.taskmap[newtask.tid] = newtask
        self.schedule(newtask)
        return newtask.tid

    def exit(self, task):
        print("Task %d terminated" % task.tid)
        del self.taskmap[task.tid]
        # Notify other tasks waiting for exit of the exiting task
        for task in self.exit_waiting.pop(task.tid, []):
            print(task)
            self.schedule(task)

    def waitforexit(self, task, waittid):
        if waittid in self.taskmap:
            self.exit_waiting.setdefault(waittid, []).append(task)
            print(self.exit_waiting)
            return True
        else:
            return False

    def schedule(self, task):
        self.ready.put(task)

    def mainloop(self):
        while self.taskmap:
            print(self.ready._qsize())
            task = self.ready.get()
            try:
                print(self.ready._qsize())
                result = task.run()
                if isinstance(result, SystemCall):
                    # task that currently running
                    result.task = task
                    result.sched = self
                    result.handle()
                    continue
            except StopIteration:
                self.exit(task)
                continue
            self.schedule(task)


# ------------------------------------------------------------
#                   === System Calls ===
# ------------------------------------------------------------


class SystemCall(object):
    def handle(self):
        pass


# Return a task's ID number
class GetTid(SystemCall):
    def handle(self):
        self.task.sendval = self.task.tid
        self.sched.schedule(self.task)


# Create a new task
class NewTask(SystemCall):
    def __init__(self, target):
        self.target = target

    def handle(self):
        tid = self.sched.new(self.target)
        self.task.sendval = tid
        self.sched.schedule(self.task)


# Kill a task
class KillTask(SystemCall):
    def __init__(self, tid):
        self.tid = tid

    def handle(self):
        task = self.sched.taskmap.get(self.tid, None)
        if task:
            task.target.close()
            self.task.sendval = True
        else:
            self.task.sendval = False
        self.sched.schedule(self.task)


# Wait for a task to exit
class WaitTask(SystemCall):
    def __init__(self, tid):
        self.tid = tid

    def handle(self):
        result = self.sched.waitforexit(self.task, self.tid)
        self.task.sendval = result
        # If waiting for a non-existent task,
        # return immediately without waiting(put the tast back to the ready queue)
        if not result:
            self.sched.schedule(self.task)


# ------------------------------------------------------------
#                      === Example ===
# ------------------------------------------------------------
if __name__ == "__main__":

    def foo():
        for i in range(5):
            print("I'm foo")
            yield

    def main():
        child = yield NewTask(foo())
        print(child)
        print("Waiting for child")
        yield WaitTask(child)
        print("Child done")


sched = Scheduler()
sched.new(main())
sched.mainloop()


"""
# ------------------------------------------------------------
                programme steps (briefly):
# ------------------------------------------------------------
1-intiate the scheduler
2-call new with main generator
3-resulting of creating new task(main) and put it into the dict and call the schedule method wich put the task(main)
to the queue 
4-call the main loop 
5-resulting pull the task from the ready queue and put it into task var 
6- run the task
7- resulting call the run method in task class wich send to the main the sendval
8- when sending to main the yeild NewTask(foo()) 
9- resulting initiating a NewTask object (foo) and set the result to that 
10- then the if condition is meet and we add new two instance to the result
(1-the task that crruntly running to latter push it back to the queue because we will not reach the self.schedule(task)
 2-the schedualar it self to call the methods from inside the handle function of newtask calss)
11- call the handle func
12- resulting 1- call the new wich create the foo Task
 2- set the sendval of the task(wich is the main task) to the foo id (tid)
 note :calling the new will aslo push the foo task to the queue
 3- call the schedule to  push the main task to the queue again 
13- next iteration we will call the foo task 
14- next iteration we will call the main task resulting to set the child to the setval wich is the foo id (2)
15- then yield WaitTask(child) take palce 
16- resultig to initite the waittask with tid of foo (2)
17- then the if condition meet so we repeat the process and then call the handle func
18- resulting calling the waitforexit and send the task wich is main and the tid wich is the tid of the foo (2)
19- reulting first check if the task we will wait for it to finish is now on the scedular or already exit 
20- if its still in the schedular we will put the task to wait in the dict (key:is the tid of the process we wait to finsh
,value: is the process that will wait) and reutrn true vice versa reutrn false
21- asing the process sendval to the result 
22- if the result is false that mean the process we waiting for is not currently in the system we immedialty push
the process to the ready queue
23- when any process exit we chick if this process cause any other process to wait for it 
if so we resume those process by putting them back to the ready queue
"""
