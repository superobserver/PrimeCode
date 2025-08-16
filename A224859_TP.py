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

A224859 = [0]*int(limit+100) #(11,13)




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

#A224859 (47,49)
# 47 
    drLD(x, 42, -1, 47, 91, A224859, 47) #47,91
    drLD(x, 78, 5, 19, 83, A224859, 47) #19,83
    drLD(x, 132, 46, 11, 37, A224859, 47) #11,37
    drLD(x, 78, 11, 29, 73, A224859, 47) #29,73
    drLD(x, 108, 26, 13, 59, A224859, 47) #13,59
    drLD(x, 72, 8, 31, 77, A224859, 47) #31,77
    drLD(x, 108, 30, 23, 49, A224859, 47) #23,49
    drLD(x, 102, 17, 7, 71, A224859, 47) #7,71
    drLD(x, 48, 0, 43, 89, A224859, 47) #43,89
    drLD(x, 102, 23, 17, 61, A224859, 47) #17,61
    drLD(x, 48, 4, 53, 79, A224859, 47) #53,79
    drLD(x, 72, 12, 41, 67, A224859, 47) #41,67
# 49 
    drLD(x, 40, -1, 49, 91, A224859, 49) #49,91
    drLD(x, 130, 46, 19, 31, A224859, 49) #19,31
    drLD(x, 76, 13, 37, 67, A224859, 49) #37,67
    drLD(x, 94, 14, 13, 73, A224859, 49) #13,73
    drLD(x, 140, 53, 11, 29, A224859, 49) #11,29
    drLD(x, 86, 20, 47, 47, A224859, 49) #47,47
    drLD(x, 14, 0, 83, 83, A224859, 49) #83,83
    drLD(x, 104, 27, 23, 53, A224859, 49) #23,53
    drLD(x, 50, 0, 41, 89, A224859, 49) #41,89
    drLD(x, 50, 6, 59, 71, A224859, 49) #59,71
    drLD(x, 86, 10, 17, 77, A224859, 49) #17,77
    drLD(x, 166, 76, 7, 7, A224859, 49) #7,7
    drLD(x, 94, 24, 43, 43, A224859, 49) #43,43
    drLD(x, 40, 3, 61, 79, A224859, 49) #61,79
 
    
    
    
    
A224859 = A224859[:-100] #(11,13)
new1 = A224859.count(0)



with open('A224859.csv', 'w', newline='') as file:
    # Step 4: Using csv.writer to write the list to the CSV file
    writer = csv.writer(file)
    writer.writerow([new1]) # Use writerow for single list

#close window
sys.exit()