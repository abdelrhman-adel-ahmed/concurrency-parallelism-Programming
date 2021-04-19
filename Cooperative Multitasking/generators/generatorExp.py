import cProfile

cProfile.run("sum([i*i for i in range(10000)])")
cProfile.run("sum((i*i for i in range(10000)))")
