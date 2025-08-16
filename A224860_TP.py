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

A224860 = [0]*int(limit+100) #(11,13)




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

#A224860 (59,61)
# 59 
    drLD(x, 30, -1, 59, 91, A224860, 59) #59,91
    drLD(x, 120, 38, 19, 41, A224860, 59) #19,41
    drLD(x, 66, 7, 37, 77, A224860, 59) #37,77
    drLD(x, 84, 12, 23, 73, A224860, 59) #23,73
    drLD(x, 90, 9, 11, 79, A224860, 59) #11,79
    drLD(x, 90, 19, 29, 61, A224860, 59) #29,61
    drLD(x, 126, 39, 7, 47, A224860, 59) #7,47
    drLD(x, 54, 3, 43, 83, A224860, 59) #43,83
    drLD(x, 114, 31, 13, 53, A224860, 59) #13,53
    drLD(x, 60, 0, 31, 89, A224860, 59) #31,89
    drLD(x, 60, 8, 49, 71, A224860, 59) #49,71
    drLD(x, 96, 18, 17, 67, A224860, 59) #17,67
# 61
    drLD(x, 28, -1, 61, 91, A224860, 61) #61,91
    drLD(x, 82, 8, 19, 79, A224860, 61) #19,79
    drLD(x, 100, 27, 37, 43, A224860, 61) #37,43)
    drLD(x, 100, 15, 7, 73, A224860, 61) #7,73
    drLD(x, 98, 16, 11, 71, A224860, 61) #11,71
    drLD(x, 62, 0, 29, 89, A224860, 61) #29,89
    drLD(x, 80, 17, 47, 53, A224860, 61) #47,53
    drLD(x, 80, 5, 17, 83, A224860, 61) #17,83
    drLD(x, 100, 19, 13, 67, A224860, 61) #13,67
    drLD(x, 118, 38, 31, 31, A224860, 61) #31,31
    drLD(x, 82, 18, 49, 49, A224860, 61) #49,49
    drLD(x, 80, 9, 23, 77, A224860, 61) #23,77
    drLD(x, 98, 26, 41, 41, A224860, 61) #41,41
    drLD(x, 62, 10, 59, 59, A224860, 61) #59,59
 
    
    
    
    
A224860 = A224860[:-100] #(11,13)
new1 = A224860.count(0)



with open('A224860.csv', 'w', newline='') as file:
    # Step 4: Using csv.writer to write the list to the CSV file
    writer = csv.writer(file)
    writer.writerow([new1]) # Use writerow for single list

#close window
sys.exit()