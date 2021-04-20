l = [1, 2, 3, 4, 5, 6, 7, 7, 2, 2, 1, 2, 3, 4, 4, 312, 321, 321, 33, 4123, 12, 312, 3, 12, 2]

"""
programme goal:
find match in the list with two function (using pipline) one function iterate over the list 
and pass the value to the other function wich check if the value matches the pattern

programme steps :
1- the nums generators get created 
2- the matches generator get created with the pattern argument and *(the nums generators)
3- the for loop over the marches generators start and resulting calling the g2 function 
4- the for loop in the f2 function that loop over the nums generator result to call the 
the g1 generator 
5- the g1 return the num to the g2 if the num == pattern the g2 yield the value back to the for 
loop to get prined 
6- repeate the process untill the list get exhausted, no value from (next(list_generator)) 
(stop iteration) get raised and for loop exist 

#note :for loop in python create iterator and then call the next function on that iterator tell it exhausted
if the for loop already gets an iterator it just call the next tell exhausting
"""


def g1(l):
    for num in l:
        yield num


def g2(pattern, g1_gen):
    for num in g1_gen:
        if num == pattern:
            yield num


nums_gen = g1(l)
matches_gen = g2(2, nums_gen)
for match in matches_gen:
    print(match)

    # use while loop
# try:
#     while True:
#         num = next(matches)
#         print(num)
# except StopIteration:
#     pass
