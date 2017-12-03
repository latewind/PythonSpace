#temp.py
from turtle import *


counter = 0
degree = 130

color('red', 'yellow')
begin_fill()
while True:
    forward(300)
    counter += 1
    left(degree)
    if abs(pos()) < 1 or counter is 3:
        print (counter,':')
        break
end_fill()
done()


'''
def fun(degree) :
    count = 0
    while True :
        degree = 360 % degree
        print (degree)
        if degree is 0 :
            break;
'''