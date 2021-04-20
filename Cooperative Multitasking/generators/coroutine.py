"""
  source --->(send data) to cor , that actually does the work 
  so we have source as datafllow and cor as the worker
"""

l = [1, 2, 3, 4, 5, 6, 7, 7, 2, 2, 1, 2, 3, 4, 4, 312, 321, 321, 33, 4123, 12, 312, 3, 12, 2]

def coroutine(fun):
  def start(*args,**kwargs):
    cr=fun(*args,**kwargs)
    next(cr)
    return cr
  return start
            
def source(l, target):
    for item in l:
        target.send(item)


@coroutine
def cor(pattern):
    while True:
        num = yield
        if num == pattern:
            print(num)


source(l, cor(2))
