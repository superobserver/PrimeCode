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

A224862 = [0]*int(limit+100) #(11,13)




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

#A224862 (71,73)
# 71
    drLD(x, 18, -1, 71, 91, A224862, 71) #71,91
    drLD(x, 72, 0, 19, 89, A224862, 71) #19,89
    drLD(x, 90, 21, 37, 53, A224862, 71) #37,53
    drLD(x, 90, 13, 17, 73, A224862, 71) #17,73
    drLD(x, 138, 51, 11, 31, A224862, 71) #11,31
    drLD(x, 102, 27, 29, 49, A224862, 71) #29,49
    drLD(x, 120, 36, 13, 47, A224862, 71) #13,47
    drLD(x, 30, 1, 67, 83, A224862, 71) #67,83
    drLD(x, 150, 61, 7, 23, A224862, 71) #7,23
    drLD(x, 78, 15, 41, 61, A224862, 71) #41,61
    drLD(x, 42, 3, 59, 79, A224862, 71) #59,79
    drLD(x, 60, 6, 43, 77, A224862, 71) #43,77
# 73 = A224862
    drLD(x, 16, -1, 73, 91, A224862, 73) #73,91
    drLD(x, 124, 41, 19, 37, A224862, 73) #19,37
    drLD(x, 146, 58, 11, 23, A224862, 73) #11,23
    drLD(x, 74, 8, 29, 77, A224862, 73) #29,77
    drLD(x, 74, 14, 47, 59, A224862, 73) #47,59
    drLD(x, 56, 3, 41, 83, A224862, 73) #41,83
    drLD(x, 106, 24, 13, 61, A224862, 73) #13,61
    drLD(x, 106, 30, 31, 43, A224862, 73) #31,43
    drLD(x, 124, 37, 7, 49, A224862, 73) #7,49
    drLD(x, 34, 2, 67, 79, A224862, 73) #67,79
    drLD(x, 74, 0, 17, 89, A224862, 73) #17,89
    drLD(x, 56, 7, 53, 71, A224862, 73) #53,71
 
    
    
    
    
A224862 = A224862[:-100] #(11,13)
new1 = A224862.count(0)



with open('A224862.csv', 'w', newline='') as file:
    # Step 4: Using csv.writer to write the list to the CSV file
    writer = csv.writer(file)
    writer.writerow([new1]) # Use writerow for single list

#close window
sys.exit()