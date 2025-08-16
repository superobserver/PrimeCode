#!/usr/bin/env python
#import turtle
import cmath
import math
#import itertools
#import collections
#from collections import Counter
import sys
#from array import *
#from csv import writer
#import turtle
#from matplotlib import pyplot as plt
#import latexify
import numpy
#numpy.set_printoptions(threshold=sys.maxsize)
import csv


#%%%%%%%%%%%%%%%%
#get a value for the limit of the range to be sieved
#limit = 10000000
limit = 3600
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

A224856 = [0]*int(limit+100) #(11,13)




 # Printing the function shows the underlying LaTeX expression.
def drLD(x, l, m, z, o, listvar, primitive):   #x=increment, l=quadratic term, m = quadratic term, z = primitive, o = primitive
  "This is a composite generating function"
  #print(A224854.count(0), x, z, o) #this is the number of possible primes at a given start position for the first iter all zero, second iter the first iter has removed some quantity
  y = 90*(x*x) - l*x + m
  if primitive == 91:
    try:
      listvar[y-1] = listvar[y-1]+1
    except:
      pass
  else:
    try:
      listvar[y] = listvar[y]+1
    except:
      print("This failed at x,z,o,y", x,z,o,y)
      pass    
  p = z+(90*(x-1))
  q = o+(90*(x-1))
  for n in range (1, int(((limit-y)/p)+1)):  
    if primitive == 91:
      listvar[(y-1)+(p*n)] = listvar[(y-1)+(p*n)]+1
    else:
      listvar[y+(p*n)] = listvar[y+(p*n)]+1
  for n in range (1, int(((limit-y)/q)+1)):
    if primitive == 91:
      listvar[(y-1)+(q*n)] = listvar[(y-1)+(q*n)]+1
    else:
      listvar[y+(q*n)] = listvar[y+(q*n)]+1


 
 
 
for x in range(1, int(new_limit.real)): # 10000 = 12; 100000 = 36; 1,000,000 = 108; 10,000,000 = 336; 100,000,000 = 1056; 1,000,000,000 = "Hey I need to checksum these tables, all hand-entered

#A224856 (29,31)
# 29 
    drLD(x, 60, -1, 29, 91, A224856, 29) #29,91
    drLD(x, 150, 62, 11, 19, A224856, 29) #11,19
    drLD(x, 96, 25, 37, 47, A224856, 29) #37,47
    drLD(x, 24, 1, 73, 83, A224856, 29) #73,83
    drLD(x, 144, 57, 13, 23, A224856, 29) #13,23
    drLD(x, 90, 20, 31, 59, A224856, 29) #31,59
    drLD(x, 90, 22, 41, 49, A224856, 29) #41,49
    drLD(x, 36, 3, 67, 77, A224856, 29) #67,77
    drLD(x, 156, 67, 7, 17, A224856, 29) #7,17
    drLD(x, 84, 19, 43, 53, A224856, 29) #43,53
    drLD(x, 30, 0, 61, 89, A224856, 29) #61,89
    drLD(x, 30, 2, 71, 79, A224856, 29) #71,79
# 31
    drLD(x, 58, -1, 31, 91, A224856, 31) #31,91
    drLD(x, 112, 32, 19, 49, A224856, 31) #19,49
    drLD(x, 130, 45, 13, 37, A224856, 31) #13,37
    drLD(x, 40, 4, 67, 73, A224856, 31) #67,73
    drLD(x, 158, 69, 11, 11, A224856, 31) #11,11
    drLD(x, 122, 41, 29, 29, A224856, 31) #29,29
    drLD(x, 50, 3, 47, 83, A224856, 31) #47,83
    drLD(x, 140, 54, 17, 23, A224856, 31) #17,23
    drLD(x, 68, 10, 41, 71, A224856, 31) #41,71
    drLD(x, 32, 0, 59, 89, A224856, 31) #59,89
    drLD(x, 50, 5, 53, 77, A224856, 31) #53,77
    drLD(x, 130, 43, 7, 43, A224856, 31) #7,43
    drLD(x, 58, 9, 61, 61, A224856, 31) #61,61
    drLD(x, 22, 1, 79, 79, A224856, 31) #79,79
 
    
    
    
    
A224856 = A224856[:-100] #(11,13)
new1 = A224856.count(0)



with open('A224856.csv', 'w', newline='') as file:
    # Step 4: Using csv.writer to write the list to the CSV file
    writer = csv.writer(file)
    writer.writerow([new1]) # Use writerow for single list

#close window
sys.exit()