
#!/usr/bin/env python
import turtle
import cmath
import math
import itertools
import collections
from collections import Counter
import sys
from array import *
from csv import writer
import turtle
from matplotlib import pyplot as plt
#import latexify
import numpy
numpy.set_printoptions(threshold=sys.maxsize)


#%%%%%%%%%%%%%%%%
#get a value for the limit of the range to be sieved
#limit = 10000000
limit = int(input("limit value here:"))                             #this value is for the "epoch" or the value associated with a "complete cycle" of all 12 cancellation operators or composite generators OR one full 'round' of Conway Primitives operating as cancellation operators
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

#%%%%%%%%%%%%%%%%
# costs memory scale of limit *is a constant (linear) scale factor* to expose composite certificates in the minimum cost the added overhead for expanding range is a sawtooth value(is it!?) 
#generate a 0-indexed injectible list of True with elements==limit (we pad the limit of the list +10 to simply calculation in the algorithm, we drop it at the end, before we enumerate (for example))
#primeTrue = [True]*int(limit+10) #the True Survivors are prime in A224854 (for example)

#appends +1 for every assigned operation of the algorithm, should count +1 for every function called under RANGE
#counter = [0]
#%%%%%%%%%%%%%%%%


A224889 = [0]*int(limit+10) #A224854 Numbers k such that 90*k + 11 are prime. CHECK #we +10 to limit as a buffer to allow an operator to go slightly out of the range and not throw an error on the "add to list" operation

 # Printing the function shows the underlying LaTeX expression.
def drLD(x, l, m, z, o, listvar, primitive):   #x=increment, l=quadratic term, m = quadratic term, z = primitive, o = primitive
  "This is a composite generating function"
  y = 90*(x*x) - l*x + m
  #print("This is y", y)
  try:
    listvar[y-1] = listvar[y-1]+1
  except:
    print("This failed at x,z,o,y", x,z,o,y)
    pass    
  p = z+(90*(x-1))
  q = o+(90*(x-1))
  for n in range (1, int(((limit-y)/p)+1)):  
    listvar[(y-1)+(p*n)] = listvar[(y-1)+(p*n)]+1
  for n in range (1, int(((limit-y)/q)+1)):
    listvar[(y-1)+(q*n)] = listvar[(y-1)+(q*n)]+1


 
 
 
for x in range(1, int(new_limit.real)): # 10000 = 12; 100000 = 36; 1,000,000 = 108; 10,000,000 = 336; 100,000,000 = 1056; 1,000,000,000 = "Hey I need to checksum these tables, all hand-entered

#A224889
    drLD(x, -2, 0, 91, 91, A224889, 91) #91,91
    drLD(x, 142, 56, 19, 19, A224889, 91) #19,19
    drLD(x, 70, 10, 37, 73, A224889, 91) #37, 73
    drLD(x, 128, 43, 11, 41, A224889, 91) #11, 41
    drLD(x, 92, 21, 29, 59, A224889, 91) #29,59
    drLD(x, 110, 32, 23, 47, A224889, 91) #23,47
    drLD(x, 20, 1, 77, 83, A224889, 91) #77,83
    drLD(x, 160, 71, 7, 13, A224889, 91) #7,13                  y=1,111,401,871 THIS IS CORRECT.... 
    drLD(x, 88, 19, 31, 61, A224889, 91) #31,61
    drLD(x, 52, 5, 49, 79, A224889, 91) #49,79
    drLD(x, 70, 12, 43, 67, A224889, 91) #43,67
    drLD(x, 110, 30, 17, 53, A224889, 91) #17,53
    drLD(x, 38, 4, 71, 71, A224889, 91) #71,71
    drLD(x, 2, 0, 89, 89, A224889, 91) #89,89

#A224889 = A224889[1:]    
A224889 = A224889[:-10] #(89,91)
print(A224889)
address = [i for i,x in enumerate(A224889) if x == 0]
print(address)
#address1 = [(i*90)+91 for i in address]
#print(address1)