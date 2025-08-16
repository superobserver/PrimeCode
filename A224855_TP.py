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

A224855 = [0]*int(limit+100) #(11,13)




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

#A224855 (17,19) 
#17
    drLD(x, 72, -1, 17, 91, A224855, 17)   #17,91
    drLD(x, 108, 29, 19, 53, A224855, 17) #19,53
    drLD(x, 72, 11, 37, 71, A224855, 17)   #37,71
    drLD(x, 18, 0, 73, 89, A224855, 17)   #73,89
    drLD(x, 102, 20, 11, 67, A224855, 17)  #11,67
    drLD(x, 138, 52, 13, 29, A224855, 17) #13,29
    drLD(x, 102, 28, 31, 47, A224855, 17)  #31,47
    drLD(x, 48, 3, 49, 83, A224855, 17)  #49,83
    drLD(x, 78, 8, 23, 79, A224855, 17)  #23,79
    drLD(x, 132, 45, 7, 41, A224855, 17) #7,41
    drLD(x, 78, 16, 43, 59, A224855, 17)   #43,59
    drLD(x, 42, 4, 61, 77, A224855, 17) #61,77   
# 19
    drLD(x, 70, -1, 19, 91, A224855, 19) #19,91
    drLD(x, 106, 31, 37, 37, A224855, 19) #37,73
    drLD(x, 34, 3, 73, 73, A224855, 19) #73,73
    drLD(x, 110, 27, 11, 59, A224855, 19) #11,59
    drLD(x, 110, 33, 29, 41, A224855, 19) #29,41
    drLD(x, 56, 6, 47, 77, A224855, 19) #47,77
    drLD(x, 74, 5, 23, 83, A224855, 19) #23,83
    drLD(x, 124, 40, 13, 43, A224855, 19) #13,43
    drLD(x, 70, 7, 31, 79, A224855, 19) #31,79
    drLD(x, 70, 13, 49, 61, A224855, 19) #49,61
    drLD(x, 106, 21, 7, 67, A224855, 19) #7,67
    drLD(x, 20, 0, 71, 89, A224855, 19) #71,89
    drLD(x, 74, 15, 53, 53, A224855, 19) #53,53
    drLD(x, 146, 59, 17, 17, A224855, 19) #17,17
 
    
    
    
    
A224855 = A224855[:-100] #(11,13)
new1 = A224855.count(0)



with open('A224855.csv', 'w', newline='') as file:
    # Step 4: Using csv.writer to write the list to the CSV file
    writer = csv.writer(file)
    writer.writerow([new1]) # Use writerow for single list

#close window
sys.exit()