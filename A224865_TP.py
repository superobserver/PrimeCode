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

A224865 = [0]*int(limit+100) #(11,13)




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

#A224865 (89,91)
# 89 = A224865
    drLD(x, 0, -1, 89, 91, A224865, 89) #89,91
    drLD(x, 90, 14, 19, 71, A224865, 89) #19,71
    drLD(x, 126, 42, 17, 37, A224865, 89) #17,37
    drLD(x, 54, 6, 53, 73, A224865, 89) #53,73
    drLD(x, 120, 35, 11, 49, A224865, 89) #11,49
    drLD(x, 120, 39, 29, 31, A224865, 89) #29,31
    drLD(x, 66, 10, 47, 67, A224865, 89) #47,67
    drLD(x, 84, 5, 13, 83, A224865, 89) #13,83
    drLD(x, 114, 34, 23, 43, A224865, 89) #23,43
    drLD(x, 60, 5, 41, 79, A224865, 89) #41,79
    drLD(x, 60, 9, 59, 61, A224865, 89) #59,61
    drLD(x, 96, 11, 7, 77, A224865, 89) #7,77
#91 = A224865
    drLD(x, -2, 0, 91, 91, A224865, 91) #91,91
    drLD(x, 142, 56, 19, 19, A224865, 91) #19,19
    drLD(x, 70, 10, 37, 73, A224865, 91) #37, 73
    drLD(x, 128, 43, 11, 41, A224865, 91) #11, 41
    drLD(x, 92, 21, 29, 59, A224865, 91) #29,59
    drLD(x, 110, 32, 23, 47, A224865, 91) #23,47
    drLD(x, 20, 1, 77, 83, A224865, 91) #77,83
    drLD(x, 160, 71, 7, 13, A224865, 91) #7,13
    drLD(x, 88, 19, 31, 61, A224865, 91) #31,61
    drLD(x, 52, 5, 49, 79, A224865, 91) #49,79
    drLD(x, 70, 12, 43, 67, A224865, 91) #43,67
    drLD(x, 110, 30, 17, 53, A224865, 91) #17,53
    drLD(x, 38, 4, 71, 71, A224865, 91) #71,71
    drLD(x, 2, 0, 89, 89, A224865, 91) #89,89
 
    
    
    
    
A224865 = A224865[:-100] #(11,13)
new1 = A224865.count(0)



with open('A224865.csv', 'w', newline='') as file:
    # Step 4: Using csv.writer to write the list to the CSV file
    writer = csv.writer(file)
    writer.writerow([new1]) # Use writerow for single list

#close window
sys.exit()