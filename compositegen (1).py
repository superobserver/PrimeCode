#!/usr/bin/env python
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



#%%%%%%%%%%%%%%%%
#get a value for the limit of the range to be sieved
#limit = 10000000
limit = int(input("limit value here:"))                             #this value is for the "epoch" or the value associated with a "complete cycle" of all 12 cancellation operators or composite generators
limit = int(limit)                                                  #convert it to an int type
#%%%%%%%%%%%%%%%%

#%%%%%%%%%%%%%%%%
#epochs are those regions closed under a full "loop" through the def's - there are 12 def's so each epoch uses all 12 (essentially the point just beyond the largest cancellation per round) alternatively, the clock makes one full revolution around 12 functions per +1 iteration
h = limit                                                           #set variable h as equivalent to "limit"
epoch = 90*(h*h) - 12*h + 1                                         #The largest element within the scope of cancellations defined by the operators
print("The epoch range is", epoch)
limit = epoch

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
#primeOmega = [0]*int(limit+20) #we use this setting for finding Big Omega underlying the distribution
#primeTrue = [True]*int(limit+10) #the True Survivors are prime in A201804 (for example)

#appends +1 for every assigned operation of the algorithm, should count +1 for every function called under RANGE
#counter = [0]
#%%%%%%%%%%%%%%%%


A201804 = [0]*int(limit+10) #A201804 Numbers k such that 90*k + 11 are prime. CHECK #we +10 to limit as a buffer to allow an operator to go slightly out of the range and not throw an error on the "add to list" operation
replist = []             #this is a list of quadratic addresses and the associated Conway Nontrivial Number cancellation frequency operator
oplist = []              #this is the number of 0's which are surviving per "round" of x  
list7 = []             #list for tracking the operator associated with conway primitive 7
list53 = []

 # Printing the function shows the underlying LaTeX expression.
def drLD(x, l, m, z, o, listvar, primitive):   #x=increment, l=quadratic term, m = quadratic term, z = primitive, o = primitive
  "This is a composite generating function"
  #print(A201804.count(0), x, z, o) #this is the number of possible primes at a given start position for the first iter all zero, second iter the first iter has removed some quantity
  y = 90*(x*x) - l*x + m
  listvar[y] = listvar[y]+1
  if z == 7:
    list7.append(y)
  p = z+(90*(x-1))
  q = o+(90*(x-1))
  for n in range (1, int(((limit-y)/p)+1)):  
    listvar[y+(p*n)] = listvar[y+(p*n)]+1
    if z == 7:
      list7.append(y+(p*n))
  for n in range (1, int(((limit-y)/q)+1)):
    listvar[y+(q*n)] = listvar[y+(q*n)]+1
    if o == 53:
      list53.append(y+(q*n))
      
  oplist.append(A201804.count(0))
  replist.append(x)
  replist.append(p)
  replist.append(q)
  replist.append(y)

 
 
 
for x in range(1, int(new_limit.real)): # 10000 = 12; 100000 = 36; 1,000,000 = 108; 10,000,000 = 336; 100,000,000 = 1056; 1,000,000,000 = "Hey I need to checksum these tables, all hand-entered

    drLD(x, 120, 34, 7, 53, A201804, 11)  #7,53  @4,  154 1
    drLD(x, 132, 48, 19, 29, A201804, 11) #19,29 @6,  144 2
    drLD(x, 120, 38, 17, 43, A201804, 11) #17,43 @8,  158 3
    drLD(x, 90, 11, 13, 77, A201804, 11)  #13,77 @11, 191 4
    drLD(x, 78, -1, 11, 91, A201804, 11)  #11,91 @11, 203 5
    drLD(x, 108, 32, 31, 41, A201804, 11) #31,41 @14, 176 6
    drLD(x, 90, 17, 23, 67, A201804, 11)  #23,67 @17, 197 7
    drLD(x, 72, 14, 49, 59, A201804, 11)  #49,59 @32, 230 8
    drLD(x, 60, 4, 37, 83, A201804, 11)   #37,83 @34, 244 9
    drLD(x, 60, 8, 47, 73, A201804, 11)   #47,73 @38, 248 10
    drLD(x, 48, 6, 61, 71, A201804, 11)   #61,71 @48, 270 11
    drLD(x, 12, 0, 79, 89, A201804, 11)   #79,89 @78, 336 12
 
 
 

#print(drLD) 
 
del A201804[-10:]
#print("The addresses for A201804 showing the amplitudes (0=prime)", A201804, "1 = semiprime (including p^2).") #for lst 200, A201804[-200:]
prime_address = [i for i,x in enumerate(A201804) if x == 0]
composite_address = [i for i,x in enumerate(A201804) if x != 0]
base10_limit = (limit*90)+11
print("This is the base-10 limit", base10_limit)
print("Big Omega as described in paper", Counter(A201804))
print("This is the number of operations", sum(A201804))
print("This is the number of composites", len(composite_address))
print("This is the number of primes", len(prime_address))
print("This is the number of quadratic addresses", int(new_limit.real)*12)
print("This is the base-10 limit/number of quadratic operators", base10_limit/(int(new_limit.real)*12))
print("This is the sq.rt. of the base-10 number", math.sqrt(base10_limit))
print("This is composites divided by primes", len(composite_address)/len(prime_address))
print("This is the prime counting function", len(prime_address)/limit)

primelist_base10 = [(i*90)+11 for i,x in enumerate(A201804) if x == 0]
composite_base10 = [(i*90)+11 for i,x in enumerate(A201804) if x > 0]

#print(prime_address)

#print(primelist_base10)#[-1])
#print(composite_base10)
#print(list(zip(*[iter(replist)]*4)))


drudge = list(zip(*[iter(replist)]*4))
plt.plot(composite_address, marker="+")
plt.plot(prime_address, marker="x")
plt.text(len(primelist_base10), limit, "The Primes", fontsize=12, color="orange")
plt.text(len(primelist_base10), len(composite_base10), "The Composites", fontsize=12, color="blue")
lengthprime = len(primelist_base10)
lengthcomp = len(composite_base10)
plt.text(lengthcomp, lengthprime, lengthprime, fontsize=12, color="orange", bbox=dict(facecolor='black', alpha=0.5))
plt.text(lengthcomp, lengthcomp, lengthcomp, fontsize=12, color="blue", bbox=dict(facecolor='black', alpha=0.5))


plt.xlabel ('Quantity')
plt.ylabel ('Address for A201804, not-A201804')
plt.show()
#plt.plot(replist)
#Sprint(list7)
plt.plot(list7, marker="o", markeredgecolor="red", markerfacecolor="blue")
plt.plot(list53, "x")
plt.text(10, 20, "function", bbox=dict(facecolor='red', alpha=0.5))
plt.show()

plt.xlabel ('BigOmega')
plt.ylabel ('Quantity')
d = collections.Counter(A201804)
plt.bar(d.keys(), d.values())
plt.show()


plt.xlabel ('Quantity')
plt.ylabel ('Address for A201804, not-A201804.')
plt.plot(drudge, marker="o")
#plt.plot(replist)
plt.plot(oplist, marker="+")
plt.show()
plt.plot(A201804, marker="o", markeredgecolor="red", markerfacecolor="blue")
plt.show()
plt.plot(primelist_base10, marker="o", markeredgecolor="red", markerfacecolor="blue")
plt.show()
#print(replist)


#x = limit#new_limit.real
#print("Term divided by worst case scenario of tests", x, (8011*(x*x)-1080*x +101)/(12*x))
#print("Epoch limit divided by number of operations", (90*(x*x)-12*x +1)/(12*x))
#print("Number of operators divided by epoch limit", (12*x)/(90*(x*x)-12*x +1))
#print("This is the number of digits of the base 10 limit,", (len((str((8011*(x*x)-1080*x +101))))))
#print("This is the number of digits of the quadratic,", (len((str((90*(x*x)-12*x +1))))))
#print("This is the number of operators divided by the length of the number, x, y, y*90+11, 12*x:", (12*x)/(len((str((8011*(x*x)-1080*x +101))))), 12*x)
#print("This is the number of operators divided by the length of the quadratic, x, y", (12*x)/(len((str((90*(x*x)-12*x +1))))), x)
"""
    length_number.append((len((str((8011*(x*x)-1080*x +101))))))
  #if z == 7:
  #  test_semi_list.append(y)
  #print(y, x)
  """
