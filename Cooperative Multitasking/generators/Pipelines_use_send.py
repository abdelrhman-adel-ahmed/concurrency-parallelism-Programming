# take care of start the generator
def coroutine(func):
    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        next(cr)
        return cr

    return start


@coroutine
def g2(pattern):
    print("generator started")
    try:
        while True:
            num = yield
            if num == pattern:
                print(num)
    except GeneratorExit:
        print("generator has been freed")



genr = g2(2)
genr.send(2)
# coroutines run forerver expect it get closed
genr.close()
