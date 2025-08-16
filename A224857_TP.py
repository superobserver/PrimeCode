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

#%%%%%%%%%%%%%%%
#the integer REAL part of the positive value is the limit for RANGE
new_limit = sol2
#%%%%%%%%%%%%%%%%

A224857 = [0]*int(limit+100) #(11,13)




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

#A224857 (41,43)
# 41 = v
    drLD(x, 48, -1, 41, 91, A224857, 41) #41,91
    drLD(x, 42, 0, 49, 89, A224857, 41) #49,89
    drLD(x, 102, 24, 19, 59, A224857, 41) #19,59
    drLD(x, 120, 39, 23, 37, A224857, 41) #23,37
    drLD(x, 108, 25, 11, 61, A224857, 41) #11,61
    drLD(x, 72, 7, 29, 79, A224857, 41) #29,79
    drLD(x, 90, 22, 43, 47, A224857, 41) #43,47
    drLD(x, 150, 62, 13, 17, A224857, 41) #13,17
    drLD(x, 78, 12, 31, 71, A224857, 41) #31,71
    drLD(x, 30, 2, 73, 77, A224857, 41) #73, 77
    drLD(x, 60, 9, 53, 67, A224857, 41) #53,67
    drLD(x, 90, 6, 7, 83, A224857, 41) #7,83
# 43
    drLD(x, 46, -1, 43, 91, A224857, 43) #43,91
    drLD(x, 154, 65, 7, 19, A224857, 43) #7,19
    drLD(x, 64, 6, 37, 79, A224857, 43) #37,79
    drLD(x, 46, 5, 61, 73, A224857, 43) #61,73
    drLD(x, 116, 32, 11, 53, A224857, 43) #11,53
    drLD(x, 134, 49, 17, 29, A224857, 43) #17,29
    drLD(x, 44, 0, 47, 89, A224857, 43) #47,89
    drLD(x, 26, 1, 71, 83, A224857, 43) #71,83
    drLD(x, 136, 50, 13, 31, A224857, 43) #13,31
    drLD(x, 64, 10, 49, 67, A224857, 43) #49,67
    drLD(x, 116, 36, 23, 41, A224857, 43) #23,41
    drLD(x, 44, 4, 59, 77, A224857, 43) #59,77
 
    
    
    
    
A224857 = A224857[:-100] #(11,13)
new1 = A224857.count(0)



with open('A224857.csv', 'w', newline='') as file:
    # Step 4: Using csv.writer to write the list to the CSV file
    writer = csv.writer(file)
    writer.writerow([new1]) # Use writerow for single list

#close window
sys.exit()