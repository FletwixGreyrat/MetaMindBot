from turtle import *
from random import randint


def dance(t):
   t.speed(10)
   t.left(randint(0, 90))
   j = 0
   while j < 8:          
       t.penup()
       t.goto(0, 0)
       t.pendown()
       i = 1
       while i < 32:
           t.forward(i)
           t.left(i/2+5)
           i += 1
       j += 1
   t.penup()
   t.goto(0, 0)


finish = 200
def startRace(t, x, y, color):
   t.color(color)
   t.shape('turtle')
   t.penup()
   t.goto(x, y)

t1 = Turtle()
t2 = Turtle()

startRace(t1, -200, -20, 'red')
startRace(t2, -200, 20, 'blue')

while t1.xcor() < finish and t2.xcor() < finish:
   t1.forward(randint(2,7))
   t2.forward(randint(2,7))

max_x = max(t1.xcor(), t2.xcor())

if max_x == t1.xcor():
   dance(t1)
else:
   dance(t2)