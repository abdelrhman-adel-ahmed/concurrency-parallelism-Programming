# This object encapsulates a running task.


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
