#!/usr/bin/env python
from multiprocessing import Process
import sys
import math
import cmath
from collections import Counter
import matplotlib.pyplot as plt 
import multiprocessing
import numpy as np
import matplotlib.pyplot as plt
#from matplotlib.animation import FuncAnimation
import time
print("Number of cpu : ", multiprocessing.cpu_count())

start = input("start value here:")
start = int(start)
limit = start+100
limit = int(limit)

#list of TRUE to depth of search space
primes = [0]*int(limit-start)


#get RANGE for number of iterations through functions
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

#the integer REAL part of this value is the limit for RANGE
new_limit = sol2




def drLD1(x):   
  "drLD(x, 78, -1, 11, 91)  #11,91 @11, 203 5    564"
  global primes
  global new_limit
  for x in range(1, int(new_limit.real)):
    y = 90*(x*x) - 78*x - 1 
    if start <= y < limit: 
      primes[y-start] = primes[y-start]+1
      print("added y", y)
 
    p =11+(90*(x-1))
    newp_start = int(((start-y)/p))
    newp_lim = int(((limit-y)/p)+1)

    for n in range(newp_start, newp_lim):
    #  s = s+1
      new_y = y+(p*n)
      if start <= new_y < limit: 
        primes[new_y - start] = primes[new_y-start]+1

    q = 91+(90*(x-1))
    newq_start = int(((start-y)/q))
    newq_lim = int(((limit-y)/q)+1)

    for n in range(newq_start, newq_lim):
    #  s = s+1
      new_y = y+(q*n)
      if start <= new_y < limit: 
        primes[new_y - start] = primes[new_y-start]+1


def drLD2():   
  "drLD(x, 120, 34, 7, 53)  #7,53  @4,  154 1    831"
  global primes
  global new_limit
  
  for x in range(1, int(new_limit.real)):
    y = 90*(x*x) - 120*x + 34 
    if start <= y < limit: 
      primes[y-start] = primes[y-start]+1
      print("added y", y)
 
    p =7+(90*(x-1))
    newp_start = int(((start-y)/p))
    newp_lim = int(((limit-y)/p)+1)

    for n in range(newp_start, newp_lim):
    #  s = s+1
      new_y = y+(p*n)
      if start <= new_y < limit: 
        primes[new_y - start] = primes[new_y-start]+1

    q = 53+(90*(x-1))
    newq_start = int(((start-y)/q))
    newq_lim = int(((limit-y)/q)+1)

    for n in range(newq_start, newq_lim):
    #  s = s+1
      new_y = y+(q*n)
      if start <= new_y < limit: 
        primes[new_y - start] = primes[new_y-start]+1

if __name__ == "__main__":
    pool1 = mp.Pool(processes=3)
    new_rows2 = pool1.starmap(sumP, [(f1, f2), (f2, f3), (f1, f3)]) 
    print(new_rows2)
"""
rocket = 0

def func1():
    global rocket
    print ('start func1')
    while rocket < sys.maxsize:
        rocket += 1
    print ('end func1')

def func2():
    global rocket
    print ('start func2')
    while rocket < sys.maxsize:
        rocket += 1
    print ('end func2')


    
    drLD(x, 132, 48, 19, 29) #19,29 @6,  144 2    371
    drLD(x, 120, 38, 17, 43) #17,43 @8,  158 3    403 
    drLD(x, 90, 11, 13, 77)  #13,77 @11, 191 4    493
    drLD(x, 108, 32, 31, 41) #31,41 @14, 176 6    262
    drLD(x, 90, 17, 23, 67)  #23,67 @17, 197 7    320
    drLD(x, 72, 14, 49, 59)  #49,59 @32, 230 8    192
    drLD(x, 60, 4, 37, 83)   #37,83 @34, 244 9    229
    drLD(x, 60, 8, 47, 73)   #47,73 @38, 248 10   195   
    drLD(x, 48, 6, 61, 71)   #61,71 @48, 270 11   165
    drLD(x, 12, 0, 79, 89)   #79,89 @78, 336 12   139
    """