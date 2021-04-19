def s():
    li = list()
    for i in range(10000):
        li.append(i)
    s = sum(li)
    return s


def g():
    li = list()
    s = 0
    for i in range(10000):
        li.append(i)
        s += li[i]
        yield s


#or use for loop it implicitly create an iterator and apply next each iteration and assign the return of the next to the loop var 
try:
    gen = g()
    while True:
        result = next(gen)
except StopIteration:
    print(result)
