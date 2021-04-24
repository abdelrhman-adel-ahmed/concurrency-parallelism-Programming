if __name__ == "__main__":

    def foo():
        for i in range(5):
            print("I'm foo")
            yield

    def main():
        child = yield NewTask(foo())
        print("Waiting for child")
        yield WaitTask(child)
        print("Child done")


sched = Scheduler()
sched.new(main())
sched.mainloop()
