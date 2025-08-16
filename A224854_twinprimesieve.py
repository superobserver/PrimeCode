#!/usr/bin/env python
import cmath
import math
import sys
import numpy
import csv
import turtle

#%%%%%%%%%%%%%%%%

limit = 20
#limit = int(input("limit value here:"))                             #this value is for the "epoch" or the value associated with a "complete cycle" of all 12 cancellation operators or composite generators OR one full 'round' of Conway Primitives operating as cancellation operators
limit = int(limit)                                                  #convert it to an int type
#%%%%%%%%%%%%%%%%

#%%%%%%%%%%%%%%%%
#epochs are those regions closed under a full "loop" through the def's - there are 12 def's so each epoch uses all 12 (essentially the point just beyond the largest cancellation per round) alternatively, the clock makes one full revolution around 12 functions per +1 iteration
h = limit                                                           #set variable h as equivalent to "limit"
epoch = 90*(h*h) - 12*h + 1                                         #The largest element within the scope of cancellations defined by the operators
print("The epoch range is", epoch)
limit = epoch
base10 = (limit*90)+11
print("This is the base-10 limit:", base10)
#%%%%%%%%%%%%%%%%

#%%%%%%%%%%%%%%%%
#get RANGE for number of iterations x through the quadratic functions (to meet the endpoints of the epoch value)
#constants for QUADRATIC
a = 90
b = -300
c = 250 - limit 
# calculate the discriminant
d = (b**2) - (4*a*c)
# find two solutions
sol1 = (-b-cmath.sqrt(d))/(2*a)
sol2 = (-b+cmath.sqrt(d))/(2*a)
print('The solution are {0} and {1}'.format(sol1,sol2))
#%%%%%%%%%%%%%%%%

#%%%%%%%%%%%%%%%%
#the integer REAL part of the positive value is the limit for RANGE
new_limit = sol2
#%%%%%%%%%%%%%%%%

A224854 = [0]*int(limit+100) #(11,13)




 # Printing the function shows the underlying LaTeX expression.
def drLD(x, l, m, z, o, listvar, primitive):   #x=increment, l=quadratic term, m = quadratic term, z = primitive, o = primitive
  "This is a composite generating function"
  y = 90*(x*x) - l*x + m
  listvar[y] = listvar[y]+1   
  p = z+(90*(x-1))
  q = o+(90*(x-1))
  for n in range (1, int(((limit-y)/p)+1)):  
    listvar[y+(p*n)] = listvar[y+(p*n)]+1
  for n in range (1, int(((limit-y)/q)+1)):
    listvar[y+(q*n)] = listvar[y+(q*n)]+1


 
 
 
for x in range(1, int(new_limit.real)): # 10000 = 12; 100000 = 36; 1,000,000 = 108; 10,000,000 = 336; 100,000,000 = 1056; 1,000,000,000 = "Hey I need to checksum these tables, all hand-entered

#A224854 (11,13)
#11
    drLD(x, 120, 34, 7, 53, A224854, 11)  #7,53  @4,  154 1
    drLD(x, 132, 48, 19, 29, A224854, 11) #19,29 @6,  144 2
    drLD(x, 120, 38, 17, 43, A224854, 11) #17,43 @8,  158 3
    drLD(x, 90, 11, 13, 77, A224854, 11)  #13,77 @11, 191 4
    drLD(x, 78, -1, 11, 91, A224854, 11)  #11,91 @11, 203 5
    drLD(x, 108, 32, 31, 41, A224854, 11) #31,41 @14, 176 6
    drLD(x, 90, 17, 23, 67, A224854, 11)  #23,67 @17, 197 7
    drLD(x, 72, 14, 49, 59, A224854, 11)  #49,59 @32, 230 8
    drLD(x, 60, 4, 37, 83, A224854, 11)   #37,83 @34, 244 9
    drLD(x, 60, 8, 47, 73, A224854, 11)   #47,73 @38, 248 10
    drLD(x, 48, 6, 61, 71, A224854, 11)   #61,71 @48, 270 11
    drLD(x, 12, 0, 79, 89, A224854, 11)   #79,89 @78, 336 12
#13
    drLD(x, 76, -1, 13, 91, A224854, 13)   #13,91
    drLD(x, 94, 18, 19, 67, A224854, 13)  #19,67
    drLD(x, 94, 24, 37, 49, A224854, 13)  #37,49
    drLD(x, 76, 11, 31, 73, A224854, 13)  #31,73
    drLD(x, 86, 6, 11, 83, A224854, 13)   #11,83
    drLD(x, 104, 29, 29, 47, A224854, 13) #29,47
    drLD(x, 86, 14, 23, 71, A224854, 13)  #23,71
    drLD(x, 86, 20, 41, 53, A224854, 13)  #41,53 
    drLD(x, 104, 25, 17, 59, A224854, 13) #17,59
    drLD(x, 14, 0, 77, 89, A224854, 13)   #77,89
    drLD(x, 94, 10, 7, 79, A224854, 13)   #7,79
    drLD(x, 76, 15, 43, 61, A224854, 13)  #43,61
 
    
A224854 = A224854[:-100] #(11,13)
new1 = A224854.count(0)
A224854a = [i for i,x in enumerate(A224854) if x == 0]
print(A224854a)


turtle.tracer(0)
turtle.bgcolor("black")
turtle.pencolor('white')

for i in A224854a:

    turtle.right(90)    # Face South
    turtle.forward(i)   # Move one radius
    turtle.right(270)   # Back to start heading
    turtle.pendown()    # Put the pen back down
    turtle.circle(i)    # Draw a circle
    turtle.penup()      # Pen up while we go home
    turtle.home()       # Head back to the start pos
turtle.exitonclick()