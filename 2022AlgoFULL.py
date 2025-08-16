#!/usr/bin/env python
import cmath
import itertools
from collections import Counter
import sys
from array import *
#import sympy
from csv import writer
import numpy as np
import matplotlib.pyplot as plt
import turtle




#%%%%%%%%%%%%%%%%
#get a value for the limit of the range to be sieved
#limit = 10000000
limit = int(input("limit value here:"))
limit = int(limit) #convert it to an int type
#%%%%%%%%%%%%%%%%

#%%%%%%%%%%%%%%%%
#epochs are those regions closed under a full "loop" through the def's - there are 12 def's so each epoch uses all 12 (essentially the point just beyond the largest cancellation per round) alternatively, the clock makes one full revolution around 12 functions per +1 iteration
h = limit
epoch = 90*(h*h) - 12*h + 1
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
# costs memory scale of limit *is a constant (linear) scale factor*
#generate a 0-indexted injectible list of True with elements==limit (we pad the limit of the list +10 to simply calculation in the algorithm, we drop it at the end, before we enumerate (for example))
#primeOmega = [0]*int(limit+20) #we use this setting for finding Big Omega underlying the distribution
#primeTrue = [True]*int(limit+10) #the True Survivors are prime in A201804 (for example)

#appends +1 for every assigned operation of the algorithm, should count +1 for every function called under RANGE
#counter = [0]
#%%%%%%%%%%%%%%%%

A181732 = [0]*int(limit+2000) #A181732 Numbers n such that 90n + 1 are prime CHECKD
A202116 = [0]*int(limit+2000) #A202116 Numbers n such that 90n + 89 is prime. CHECKD
A196007 = [0]*int(limit+2000) #A196007 Numbers n such that 90n + 83 is prime. CHECKD
A202112 = [0]*int(limit+2000) #A202112 Numbers n such that 90n + 79 is prime. CHECKD
A201822 = [0]*int(limit+2000) #A201822 Numbers k such that 90*k + 77 is prime. CHECKD
A195993 = [0]*int(limit+2000) #A195993 Numbers n such that 90n + 73 is prime. CHECKD
A202129 = [0]*int(limit+2000) #A202129 Numbers n such that 90n + 71 is prime. CHECKD
A201817 = [0]*int(limit+2000) #A201817 Numbers k such that 90*k + 67 is prime. CHECKD
A202113 = [0]*int(limit+2000) #A202113 Numbers n such that 90n + 61 is prime. CHECKD
A202101 = [0]*int(limit+2000) #A202101 Numbers n such that 90*n + 59 is prime. CHECKD
A202114 = [0]*int(limit+2000) #A202114 Numbers n such that 90n + 53 is prime. CHECKD see:A142316
A201818 = [0]*int(limit+2000) #A201818 Numbers k such that 90*k + 49 is prime.CHECKD
A201734 = [0]*int(limit+2000) #A201734 Numbers n such that 90*n + 47 is prime. CHECKD 
A202105 = [0]*int(limit+2000) #A202105 Numbers n such that 90*n + 43 is prime. CHECKD
A202104 = [0]*int(limit+2000) #A202104 Numbers n such that 90*n + 41 is prime. CHECKD
A198382 = [0]*int(limit+2000) #A198382 Numbers n such that 90n + 37 is prime. CHECKD
A201819 = [0]*int(limit+2000) #A201819 Numbers n such that 90*n + 31 is prime. CHECKD
A201739 = [0]*int(limit+2000) #A201739 Numbers n such that 90*n + 29 is prime. CHECKD
A201820 = [0]*int(limit+2000) #A201820 Numbers k such that 90*k + 23 is prime. CHECKD
A196000 = [0]*int(limit+2000) #A196000 Numbers n such that 90n + 19 is prime. CHECKD
A202115 = [0]*int(limit+2000) #A202115 Numbers n such that 90n + 17 is prime. CHECKD
A201816 = [0]*int(limit+2000) #A201816 Numbers k such that 90*k + 13 is prime. CHECKD
A201804 = [0]*int(limit+2000) #A201804 Numbers k such that 90*k + 11 are prime. CHECKD
A202110 = [0]*int(limit+2000) #A202110 Numbers n such that 90*n + 7 is prime. CHECKD see:A142315












#%%%%%%%%%%%%%%%%
#here comes a function for generating composites
def drLD(x, l, m, z, o, listvar, primitive):   #x=increment, l=quadratic term, m = quadratic term, z = primitive, o = primitive
  "This is a composite generating function"
  y = 90*(x*x) - l*x + m
  #primeOmega[y] = primeOmega[y]+1
  listvar[y] = listvar[y]+1
  #primeTrue[y] = False
  p = z+(90*(x-1))
  for n in range (1, int(((limit-y)/p)+1)):
   # primeOmega[y+(p*n)] = primeOmega[y+(p*n)]+1
    listvar[y+(p*n)] = listvar[y+(p*n)]+1
  #  primeTrue[y+(p*n)] = False
  q = o+(90*(x-1))
  for n in range (1, int(((limit-y)/q)+1)):
    #primeOmega[y+(q*n)] = primeOmega[y+(q*n)]+1
    listvar[y+(q*n)] = listvar[y+(q*n)]+1
   # primeTrue[y+(q*n)] = False
  #print((sum(primeTrue)-10, y, x, z, o, p, q, limit))#, (limit-y)/p,  (limit-y)/q))#-int(new_limit.real)), y, x, z, o, p, q, limit)

#%%%%%%%%%%%%%%%%










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


#13 = b
    drLD(x, 76, -1, 13, 91, A201816, 13)   #13,91
    drLD(x, 94, 18, 19, 67, A201816, 13)  #19,67
    drLD(x, 94, 24, 37, 49, A201816, 13)  #37,49
    drLD(x, 76, 11, 31, 73, A201816, 13)  #31,73
    drLD(x, 86, 6, 11, 83, A201816, 13)   #11,83
    drLD(x, 104, 29, 29, 47, A201816, 13) #29,47
    drLD(x, 86, 14, 23, 71, A201816, 13)  #23,71
    drLD(x, 86, 20, 41, 53, A201816, 13)  #41,53
    drLD(x, 104, 25, 17, 59, A201816, 13) #17,59
    drLD(x, 14, 0, 77, 89, A201816, 13)   #77,89
    drLD(x, 94, 10, 7, 79, A201816, 13)   #7,79
    drLD(x, 76, 15, 43, 61, A201816, 13) #43,61

#17 = c
    drLD(x, 72, -1, 17, 91, A202115, 17)   #17,91
    drLD(x, 108, 29, 19, 53, A202115, 17) #19,53
    drLD(x, 72, 11, 37, 71, A202115, 17)   #37,71
    drLD(x, 18, 0, 73, 89, A202115, 17)   #73,89
    drLD(x, 102, 20, 11, 67, A202115, 17)  #11,67
    drLD(x, 138, 52, 13, 29, A202115, 17) #13,29
    drLD(x, 102, 28, 31, 47, A202115, 17)  #31,47
    drLD(x, 48, 3, 49, 83, A202115, 17)  #49,83
    drLD(x, 78, 8, 23, 79, A202115, 17)  #23,79
    drLD(x, 132, 45, 7, 41, A202115, 17) #7,41
    drLD(x, 78, 16, 43, 59, A202115, 17)   #43,59
    drLD(x, 42, 4, 61, 77, A202115, 17) #61,77   

#91 = A181732
    drLD(x, -2, 0, 91, 91, A181732, 91) #91,91
    drLD(x, 142, 56, 19, 19, A181732, 91) #19,19
    drLD(x, 70, 10, 37, 73, A181732, 91) #37, 73
    drLD(x, 128, 43, 11, 41, A181732, 91) #11, 41
    drLD(x, 92, 21, 29, 59, A181732, 91) #29,59
    drLD(x, 110, 32, 23, 47, A181732, 91) #23,47
    drLD(x, 20, 1, 77, 83, A181732, 91) #77,83
    drLD(x, 160, 71, 7, 13, A181732, 91) #7,13
    drLD(x, 88, 19, 31, 61, A181732, 91) #31,61
    drLD(x, 52, 5, 49, 79, A181732, 91) #49,79
    drLD(x, 70, 12, 43, 67, A181732, 91) #43,67
    drLD(x, 110, 30, 17, 53, A181732, 91) #17,53
    drLD(x, 38, 4, 71, 71, A181732, 91) #71,71
    drLD(x, 2, 0, 89, 89, A181732, 91) #89,89

# 89 = A202116
    drLD(x, 0, -1, 89, 91, A202116, 89) #89,91
    drLD(x, 90, 14, 19, 71, A202116, 89) #19,71
    drLD(x, 126, 42, 17, 37, A202116, 89) #17,37
    drLD(x, 54, 6, 53, 73, A202116, 89) #53,73
    drLD(x, 120, 35, 11, 49, A202116, 89) #11,49
    drLD(x, 120, 39, 29, 31, A202116, 89) #29,31
    drLD(x, 66, 10, 47, 67, A202116, 89) #47,67
    drLD(x, 84, 5, 13, 83, A202116, 89) #13,83
    drLD(x, 114, 34, 23, 43, A202116, 89) #23,43
    drLD(x, 60, 5, 41, 79, A202116, 89) #41,79
    drLD(x, 60, 9, 59, 61, A202116, 89) #59,61
    drLD(x, 96, 11, 7, 77, A202116, 89) #7,77

# 83 = f
    drLD(x, 6, -1, 83, 91, A196007, 83) #83,91
    drLD(x, 114, 33, 19, 47, A196007, 83) #19,47
    drLD(x, 114, 35, 29, 37, A196007, 83) #37,29
    drLD(x, 96, 14, 11, 73, A196007, 83) #11,73
    drLD(x, 126, 41, 13, 41, A196007, 83) #13,41
    drLD(x, 126, 43, 23, 31, A196007, 83) #23,31
    drLD(x, 54, 5, 49, 77, A196007, 83) #49,77
    drLD(x, 54, 7, 59, 67, A196007, 83) #59,67
    drLD(x, 84, 0, 7, 89, A196007, 83) #7,89
    drLD(x, 66, 9, 43, 71, A196007, 83) #43,71
    drLD(x, 66, 11, 53, 61, A196007, 83) #53,61
    drLD(x, 84, 8, 17, 79, A196007, 83) #17,79



# 79 = A202112
    drLD(x, 10, -1, 79, 91, A202112, 79) #79,91
    drLD(x, 100, 22, 19, 61, A202112, 79) #19,61
    drLD(x, 136, 48, 7, 37, A202112, 79) #7,37
    drLD(x, 64, 8, 43, 73, A202112, 79) #43,73
    drLD(x, 80, 0, 11, 89, A202112, 79) #11,89
    drLD(x, 80, 12, 29, 71, A202112, 79) #29,71
    drLD(x, 116, 34, 17, 47, A202112, 79) #17,47
    drLD(x, 44, 2, 53, 83, A202112, 79) #53,83
    drLD(x, 154, 65, 13, 13, A202112, 79) #13,13
    drLD(x, 100, 26, 31, 49, A202112, 79) #31,49
    drLD(x, 46, 5, 67, 67, A202112, 79) #67,67
    drLD(x, 134, 49, 23, 23, A202112, 79) #23,23
    drLD(x, 80, 16, 41, 59, A202112, 79) #41,59
    drLD(x, 26, 1, 77, 77, A202112, 79) #77,77


# 77 = h
    drLD(x, 12, -1, 77, 91, A201822, 79) #77,91
    drLD(x, 138, 52, 19, 23, A201822, 79) #19,23
    drLD(x, 102, 28, 37, 41, A201822, 79) #37,41
    drLD(x, 48, 5, 59, 73, A201822, 79) #59,73
    drLD(x, 162, 72, 7, 11, A201822, 79) #7,11
    drLD(x, 108, 31, 29, 43, A201822, 79) #29,43
    drLD(x, 72, 13, 47, 61, A201822, 79) #47,61
    drLD(x, 18, 0, 79, 83, A201822, 79) #79,83
    drLD(x, 78, 0, 13, 89, A201822, 79) #13,89
    drLD(x, 132, 47, 17, 31, A201822, 79) #17,31
    drLD(x, 78, 16, 49, 53, A201822, 79) #49,53
    drLD(x, 42, 4, 67, 71, A201822, 79) #67,71

# 73 = A195993
    drLD(x, 16, -1, 73, 91, A195993, 73) #73,91
    drLD(x, 124, 41, 19, 37, A195993, 73) #19,37
    drLD(x, 146, 58, 11, 23, A195993, 73) #11,23
    drLD(x, 74, 8, 29, 77, A195993, 73) #29,77
    drLD(x, 74, 14, 47, 59, A195993, 73) #47,59
    drLD(x, 56, 3, 41, 83, A195993, 73) #41,83
    drLD(x, 106, 24, 13, 61, A195993, 73) #13,61
    drLD(x, 106, 30, 31, 43, A195993, 73) #31,43
    drLD(x, 124, 37, 7, 49, A195993, 73) #7,49
    drLD(x, 34, 2, 67, 79, A195993, 73) #67,79
    drLD(x, 74, 0, 17, 89, A195993, 73) #17,89
    drLD(x, 56, 7, 53, 71, A195993, 73) #53,71


# 71 = j
    drLD(x, 18, -1, 71, 91, A202129, 71) #71,91
    drLD(x, 72, 0, 19, 89, A202129, 71) #19,89
    drLD(x, 90, 21, 37, 53, A202129, 71) #37,53
    drLD(x, 90, 13, 17, 73, A202129, 71) #17,73
    drLD(x, 138, 51, 11, 31, A202129, 71) #11,31
    drLD(x, 102, 27, 29, 49, A202129, 71) #29,49
    drLD(x, 120, 36, 13, 47, A202129, 71) #13,47
    drLD(x, 30, 1, 67, 83, A202129, 71) #67,83
    drLD(x, 150, 61, 7, 23, A202129, 71) #7,23
    drLD(x, 78, 15, 41, 61, A202129, 71) #41,61
    drLD(x, 42, 3, 59, 79, A202129, 71) #59,79
    drLD(x, 60, 6, 43, 77, A202129, 71) #43,77

# 67 = A201817
    drLD(x, 22, -1, 67, 91, A201817, 67) #67,91
    drLD(x, 148, 60, 13, 19, A201817, 67) #13,19
    drLD(x, 112, 34, 31, 37, A201817, 67) #31,37
    drLD(x, 58, 7, 49, 73, A201817, 67) #49,73
    drLD(x, 122, 37, 11, 47, A201817, 67) #11,47
    drLD(x, 68, 4, 29, 83, A201817, 67) #29,83
    drLD(x, 122, 39, 17, 41, A201817, 67) #17,41
    drLD(x, 68, 12, 53, 59, A201817, 67) #53,59
    drLD(x, 32, 2, 71, 77, A201817, 67) #71,77
    drLD(x, 112, 26, 7, 61, A201817, 67) #7,61
    drLD(x, 58, 5, 43, 79, A201817, 67) #43,79
    drLD(x, 68, 0, 23, 89, A201817, 67) #23,89

# 61 = q
    drLD(x, 28, -1, 61, 91, A202113, 61) #61,91
    drLD(x, 82, 8, 19, 79, A202113, 61) #19,79
    drLD(x, 100, 27, 37, 43, A202113, 61) #37,43)
    drLD(x, 100, 15, 7, 73, A202113, 61) #7,73
    drLD(x, 98, 16, 11, 71, A202113, 61) #11,71
    drLD(x, 62, 0, 29, 89, A202113, 61) #29,89
    drLD(x, 80, 17, 47, 53, A202113, 61) #47,53
    drLD(x, 80, 5, 17, 83, A202113, 61) #17,83
    drLD(x, 100, 19, 13, 67, A202113, 61) #13,67
    drLD(x, 118, 38, 31, 31, A202113, 61) #31,31
    drLD(x, 82, 18, 49, 49, A202113, 61) #49,49
    drLD(x, 80, 9, 23, 77, A202113, 61) #23,77
    drLD(x, 98, 26, 41, 41, A202113, 61) #41,41
    drLD(x, 62, 10, 59, 59, A202113, 61) #59,59


# 59 = p
    drLD(x, 30, -1, 59, 91, A202101, 59) #59,91
    drLD(x, 120, 38, 19, 41, A202101, 59) #19,41
    drLD(x, 66, 7, 37, 77, A202101, 59) #37,77
    drLD(x, 84, 12, 23, 73, A202101, 59) #23,73
    drLD(x, 90, 9, 11, 79, A202101, 59) #11,79
    drLD(x, 90, 19, 29, 61, A202101, 59) #29,61
    drLD(x, 126, 39, 7, 47, A202101, 59) #7,47
    drLD(x, 54, 3, 43, 83, A202101, 59) #43,83
    drLD(x, 114, 31, 13, 53, A202101, 59) #13,53
    drLD(x, 60, 0, 31, 89, A202101, 59) #31,89
    drLD(x, 60, 8, 49, 71, A202101, 59) #49,71
    drLD(x, 96, 18, 17, 67, A202101, 59) #17,67

# 53 = r
    drLD(x, 36, -1, 53, 91, A202114, 53) #53,91
    drLD(x, 144, 57, 17, 19, A202114, 53) #17,19
    drLD(x, 54, 0, 37, 89, A202114, 53) #37,89
    drLD(x, 36, 3, 71, 73, A202114, 53) #71,73
    drLD(x, 156, 67, 11, 13, A202114, 53) #11,13
    drLD(x, 84, 15, 29, 67, A202114, 53) #29,67
    drLD(x, 84, 19, 47, 49, A202114, 53) #47,49
    drLD(x, 66, 4, 31, 83, A202114, 53) #31,83
    drLD(x, 96, 21, 23, 61, A202114, 53) #23,61
    drLD(x, 96, 25, 41, 43, A202114, 53) #41,43
    drLD(x, 114, 28, 7, 59, A202114, 53) #7,59
    drLD(x, 24, 1, 77, 79, A202114, 53) #77,79

# 49 = s
    drLD(x, 40, -1, 49, 91, A201818, 49) #49,91
    drLD(x, 130, 46, 19, 31, A201818, 49) #19,31
    drLD(x, 76, 13, 37, 67, A201818, 49) #37,67
    drLD(x, 94, 14, 13, 73, A201818, 49) #13,73
    drLD(x, 140, 53, 11, 29, A201818, 49) #11,29
    drLD(x, 86, 20, 47, 47, A201818, 49) #47,47
    drLD(x, 14, 0, 83, 83, A201818, 49) #83,83
    drLD(x, 104, 27, 23, 53, A201818, 49) #23,53
    drLD(x, 50, 0, 41, 89, A201818, 49) #41,89
    drLD(x, 50, 6, 59, 71, A201818, 49) #59,71
    drLD(x, 86, 10, 17, 77, A201818, 49) #17,77
    drLD(x, 166, 76, 7, 7, A201818, 49) #7,7
    drLD(x, 94, 24, 43, 43, A201818, 49) #43,43
    drLD(x, 40, 3, 61, 79, A201818, 49) #61,79

# 47 = t
    drLD(x, 42, -1, 47, 91, A201734, 47) #47,91
    drLD(x, 78, 5, 19, 83, A201734, 47) #19,83
    drLD(x, 132, 46, 11, 37, A201734, 47) #11,37
    drLD(x, 78, 11, 29, 73, A201734, 47) #29,73
    drLD(x, 108, 26, 13, 59, A201734, 47) #13,59
    drLD(x, 72, 8, 31, 77, A201734, 47) #31,77
    drLD(x, 108, 30, 23, 49, A201734, 47) #23,49
    drLD(x, 102, 17, 7, 71, A201734, 47) #7,71
    drLD(x, 48, 0, 43, 89, A201734, 47) #43,89
    drLD(x, 102, 23, 17, 61, A201734, 47) #17,61
    drLD(x, 48, 4, 53, 79, A201734, 47) #53,79
    drLD(x, 72, 12, 41, 67, A201734, 47) #41,67


# 43 = u
    drLD(x, 46, -1, 43, 91, A202105, 43) #43,91
    drLD(x, 154, 65, 7, 19, A202105, 43) #7,19
    drLD(x, 64, 6, 37, 79, A202105, 43) #37,79
    drLD(x, 46, 5, 61, 73, A202105, 43) #61,73
    drLD(x, 116, 32, 11, 53, A202105, 43) #11,53
    drLD(x, 134, 49, 17, 29, A202105, 43) #17,29
    drLD(x, 44, 0, 47, 89, A202105, 43) #47,89
    drLD(x, 26, 1, 71, 83, A202105, 43) #71,83
    drLD(x, 136, 50, 13, 31, A202105, 43) #13,31
    drLD(x, 64, 10, 49, 67, A202105, 43) #49,67
    drLD(x, 116, 36, 23, 41, A202105, 43) #23,41
    drLD(x, 44, 4, 59, 77, A202105, 43) #59,77

# 41 = v
    drLD(x, 48, -1, 41, 91, A202104, 41) #41,91
    drLD(x, 42, 0, 49, 89, A202104, 41) #49,89
    drLD(x, 102, 24, 19, 59, A202104, 41) #19,59
    drLD(x, 120, 39, 23, 37, A202104, 41) #23,37
    drLD(x, 108, 25, 11, 61, A202104, 41) #11,61
    drLD(x, 72, 7, 29, 79, A202104, 41) #29,79
    drLD(x, 90, 22, 43, 47, A202104, 41) #43,47
    drLD(x, 150, 62, 13, 17, A202104, 41) #13,17
    drLD(x, 78, 12, 31, 71, A202104, 41) #31,71
    drLD(x, 30, 2, 73, 77, A202104, 41) #73, 77
    drLD(x, 60, 9, 53, 67, A202104, 41) #53,67
    drLD(x, 90, 6, 7, 83, A202104, 41) #7,83

# 37 = w
    drLD(x, 52, -1, 37, 91, A198382, 37) #37,91
    drLD(x, 88, 13, 19, 73, A198382, 37) #19,73
    drLD(x, 92, 11, 11, 77, A198382, 37) #11,77
    drLD(x, 128, 45, 23, 29, A198382, 37) #23,29
    drLD(x, 92, 23, 41, 47, A198382, 37) #41,47
    drLD(x, 38, 2, 59, 83, A198382, 37) #59,83
    drLD(x, 88, 9, 13, 79, A198382, 37) #13,79
    drLD(x, 142, 54, 7, 31, A198382, 37) #7,31
    drLD(x, 88, 21, 43, 49, A198382, 37) #43,49
    drLD(x, 52, 7, 61, 67, A198382, 37) #61,67
    drLD(x, 92, 15, 17, 71, A198382, 37) #17,71
    drLD(x, 38, 0, 53, 89, A198382, 37) #53,89

# 31 = ww
    drLD(x, 58, -1, 31, 91, A201819, 31) #31,91
    drLD(x, 112, 32, 19, 49, A201819, 31) #19,49
    drLD(x, 130, 45, 13, 37, A201819, 31) #13,37
    drLD(x, 40, 4, 67, 73, A201819, 31) #67,73
    drLD(x, 158, 69, 11, 11, A201819, 31) #11,11
    drLD(x, 122, 41, 29, 29, A201819, 31) #29,29
    drLD(x, 50, 3, 47, 83, A201819, 31) #47,83
    drLD(x, 140, 54, 17, 23, A201819, 31) #17,23
    drLD(x, 68, 10, 41, 71, A201819, 31) #41,71
    drLD(x, 32, 0, 59, 89, A201819, 31) #59,89
    drLD(x, 50, 5, 53, 77, A201819, 31) #53,77
    drLD(x, 130, 43, 7, 43, A201819, 31) #7,43
    drLD(x, 58, 9, 61, 61, A201819, 31) #61,61
    drLD(x, 22, 1, 79, 79, A201819, 31) #79,79

# 29 = www
    drLD(x, 60, -1, 29, 91, A201739, 29) #29,91
    drLD(x, 150, 62, 11, 19, A201739, 29) #11,19
    drLD(x, 96, 25, 37, 47, A201739, 29) #37,47
    drLD(x, 24, 1, 73, 83, A201739, 29) #73,83
    drLD(x, 144, 57, 13, 23, A201739, 29) #13,23
    drLD(x, 90, 20, 31, 59, A201739, 29) #31,59
    drLD(x, 90, 22, 41, 49, A201739, 29) #41,49
    drLD(x, 36, 3, 67, 77, A201739, 29) #67,77
    drLD(x, 156, 67, 7, 17, A201739, 29) #7,17
    drLD(x, 84, 19, 43, 53, A201739, 29) #43,53
    drLD(x, 30, 0, 61, 89, A201739, 29) #61,89
    drLD(x, 30, 2, 71, 79, A201739, 29) #71,79

# 23 = wx
    drLD(x, 66, -1, 23, 91, A201820, 23) #23,91
    drLD(x, 84, 10, 19, 77, A201820, 23) #19,77
    drLD(x, 84, 18, 37, 59, A201820, 23) #37,59
    drLD(x, 66, 9, 41, 73, A201820, 23) #41,73
    drLD(x, 126, 41, 11, 43, A201820, 23) #11,43
    drLD(x, 144, 56, 7, 29, A201820, 23) #7,29
    drLD(x, 54, 5, 47, 79, A201820, 23) #47,79
    drLD(x, 36, 2, 61, 83, A201820, 23) #61,83
    drLD(x, 96, 16, 13, 71, A201820, 23) #13,71
    drLD(x, 96, 24, 31, 53, A201820, 23) #31,53
    drLD(x, 114, 33, 17, 49, A201820, 23) #17,49
    drLD(x, 24, 0, 67, 89, A201820, 23) #67,89

# 19 = gg
    drLD(x, 70, -1, 19, 91, A196000, 19) #19,91
    drLD(x, 106, 31, 37, 37, A196000, 19) #37,73
    drLD(x, 34, 3, 73, 73, A196000, 19) #73,73
    drLD(x, 110, 27, 11, 59, A196000, 19) #11,59
    drLD(x, 110, 33, 29, 41, A196000, 19) #29,41
    drLD(x, 56, 6, 47, 77, A196000, 19) #47,77
    drLD(x, 74, 5, 23, 83, A196000, 19) #23,83
    drLD(x, 124, 40, 13, 43, A196000, 19) #13,43
    drLD(x, 70, 7, 31, 79, A196000, 19) #31,79
    drLD(x, 70, 13, 49, 61, A196000, 19) #49,61
    drLD(x, 106, 21, 7, 67, A196000, 19) #7,67
    drLD(x, 20, 0, 71, 89, A196000, 19) #71,89
    drLD(x, 74, 15, 53, 53, A196000, 19) #53,53
    drLD(x, 146, 59, 17, 17, A196000, 19) #17,17


# 7 = xy
    drLD(x, 82, -1, 7, 91, A202110, 7) #7,91
    drLD(x, 118, 37, 19, 43, A202110, 7) #19,43
    drLD(x, 82, 17, 37, 61, A202110, 7) #37,61
    drLD(x, 28, 2, 73, 79, A202110, 7) #73,79
    drLD(x, 152, 64, 11, 17, A202110, 7) #11,17
    drLD(x, 98, 25, 29, 53, A202110, 7) #29,53
    drLD(x, 62, 9, 47, 71, A202110, 7) #47,71
    drLD(x, 8, 0, 83, 89, A202110, 7) #83,89
    drLD(x, 118, 35, 13, 49, A202110, 7) #13,49
    drLD(x, 82, 15, 31, 67, A202110, 7) #31,67
    drLD(x, 98, 23, 23, 59, A202110, 7) #23,59
    drLD(x, 62, 7, 41, 77, A202110, 7) #41,77










del A181732[-2000:]# = [91]*int(limit+10) #A181732 Numbers n such that 90n + 1 are prime CHECKD
del A202116[-2000:]# = [89]*int(limit+10) #A202116 Numbers n such that 90n + 89 is prime. CHECKD
del A196007[-2000:]# = [83]*int(limit+10) #A196007 Numbers n such that 90n + 83 is prime. CHECKD
del A202112[-2000:]# = [79]*int(limit+10) #A202112 Numbers n such that 90n + 79 is prime. CHECKD
del A201822[-2000:]# = [77]*int(limit+10) #A201822 Numbers k such that 90*k + 77 is prime. CHECKD
del A195993[-2000:]# = [73]*int(limit+10) #A195993 Numbers n such that 90n + 73 is prime. CHECKD
del A202129[-2000:]# = [71]*int(limit+10) #A202129 Numbers n such that 90n + 71 is prime. CHECKD
del A201817[-2000:]# = [67]*int(limit+10) #A201817 Numbers k such that 90*k + 67 is prime. CHECKD
del A202113[-2000:]# = [61]*int(limit+10) #A202113 Numbers n such that 90n + 61 is prime. CHECKD
del A202101[-2000:]# = [59]*int(limit+10) #A202101 Numbers n such that 90*n + 59 is prime. CHECKD
del A202114[-2000:]# = [53]*int(limit+10) #A202114 Numbers n such that 90n + 53 is prime. CHECKD see:A142316
del A201818[-2000:]# = [49]*int(limit+10) #A201818 Numbers k such that 90*k + 49 is prime.CHECKD
del A201734[-2000:]# = [47]*int(limit+10) #A201734 Numbers n such that 90*n + 47 is prime. CHECKD 
del A202105[-2000:]# = [43]*int(limit+10) #A202105 Numbers n such that 90*n + 43 is prime. CHECKD
del A202104[-2000:]# = [41]*int(limit+10) #A202104 Numbers n such that 90*n + 41 is prime. CHECKD
del A198382[-2000:]# = [37]*int(limit+10) #A198382 Numbers n such that 90n + 37 is prime. CHECKD
del A201819[-2000:]# = [31]*int(limit+10) #A201819 Numbers n such that 90*n + 31 is prime. CHECKD
del A201739[-2000:]# = [29]*int(limit+10) #A201739 Numbers n such that 90*n + 29 is prime. CHECKD
del A201820[-2000:]# = [23]*int(limit+10) #A201820 Numbers k such that 90*k + 23 is prime. CHECKD
del A196000[-2000:]# = [19]*int(limit+10) #A196000 Numbers n such that 90n + 19 is prime. CHECKD
del A202115[-2000:]# = [17]*int(limit+10) #A202115 Numbers n such that 90n + 17 is prime. CHECKD 
del A201816[-2000:]# = [13]*int(limit+10) #A201816 Numbers k such that 90*k + 13 is prime. CHECKD
del A201804[-2000:]# = [11]*int(limit+10) #A201804 Numbers k such that 90*k + 11 are prime. CHECKD
del A202110[-2000:]# = [7]*int(limit+10) #A202110 Numbers n such that 90*n + 7 is prime. CHECKD see:A142315



A181732a =[i for i,x in enumerate(A181732) if x == 0]
A202116a=[i for i,x in enumerate(A202116) if x == 0]
A196007a=[i for i,x in enumerate(A196007) if x == 0]
A202112a=[i for i,x in enumerate(A202112) if x == 0]
A201822a=[i for i,x in enumerate(A201822) if x == 0]
A195993a=[i for i,x in enumerate(A195993) if x == 0]
A202129a=[i for i,x in enumerate(A202129) if x == 0]
A201817a=[i for i,x in enumerate(A201817) if x == 0]
A202113a=[i for i,x in enumerate(A202113) if x == 0]
A202101a=[i for i,x in enumerate(A202101) if x == 0]
A202114a=[i for i,x in enumerate(A202114) if x == 0]
A201818a=[i for i,x in enumerate(A201818) if x == 0]
A201734a=[i for i,x in enumerate(A201734) if x == 0]
A202105a=[i for i,x in enumerate(A202105) if x == 0]
A202104a=[i for i,x in enumerate(A202104) if x == 0]
A198382a=[i for i,x in enumerate(A198382) if x == 0]
A201819a=[i for i,x in enumerate(A201819) if x == 0]
A201739a=[i for i,x in enumerate(A201739) if x == 0]
A201820a=[i for i,x in enumerate(A201820) if x == 0]
A196000a=[i for i,x in enumerate(A196000) if x == 0]
A202115a=[i for i,x in enumerate(A202115) if x == 0]
A201816a=[i for i,x in enumerate(A201816) if x == 0]
A201804a=[i for i,x in enumerate(A201804) if x == 0]
A202110a=[i for i,x in enumerate(A202110) if x == 0]

A181732c =[i for i,x in enumerate(A181732) if x != 0]
print(A181732c)
A202116c=[i for i,x in enumerate(A202116) if x != 0]
A196007c=[i for i,x in enumerate(A196007) if x != 0]
A202112c=[i for i,x in enumerate(A202112) if x != 0]
A201822c=[i for i,x in enumerate(A201822) if x != 0]
A195993c=[i for i,x in enumerate(A195993) if x != 0]
A202129c=[i for i,x in enumerate(A202129) if x != 0]
A201817c=[i for i,x in enumerate(A201817) if x != 0]
A202113c=[i for i,x in enumerate(A202113) if x != 0]
A202101c=[i for i,x in enumerate(A202101) if x != 0]
A202114c=[i for i,x in enumerate(A202114) if x != 0]
A201818c=[i for i,x in enumerate(A201818) if x != 0]
A201734c=[i for i,x in enumerate(A201734) if x != 0]
A202105c=[i for i,x in enumerate(A202105) if x != 0]
A202104c=[i for i,x in enumerate(A202104) if x != 0]
A198382c=[i for i,x in enumerate(A198382) if x != 0]
A201819c=[i for i,x in enumerate(A201819) if x != 0]
A201739c=[i for i,x in enumerate(A201739) if x != 0]
A201820c=[i for i,x in enumerate(A201820) if x != 0]
A196000c=[i for i,x in enumerate(A196000) if x != 0]
A202115c=[i for i,x in enumerate(A202115) if x != 0]
A201816c=[i for i,x in enumerate(A201816) if x != 0]
A201804c=[i for i,x in enumerate(A201804) if x != 0]
A202110c=[i for i,x in enumerate(A202110) if x != 0]



A181732b=[(i*90)+1 for i in A181732a] #[(i*90)+11 for i in A201804]#
A202116b=[(i*90)+89 for i in A202116a]
A196007b=[(i*90)+83 for i in A196007a]
A202112b=[(i*90)+79 for i in A202112a]
A201822b=[(i*90)+77 for i in A201822a]
A195993b=[(i*90)+73 for i in A195993a]
A202129b=[(i*90)+71 for i in A202129a]
A201817b=[(i*90)+67 for i in A201817a]
A202113b=[(i*90)+61 for i in A202113a]
A202101b=[(i*90)+59 for i in A202101a]
A202114b=[(i*90)+53 for i in A202114a]
A201818b=[(i*90)+49 for i in A201818a]
A201734b=[(i*90)+47 for i in A201734a]
A202105b=[(i*90)+43 for i in A202105a]
A202104b=[(i*90)+41 for i in A202104a]
A198382b=[(i*90)+37 for i in A198382a]
A201819b=[(i*90)+31 for i in A201819a]
A201739b=[(i*90)+29 for i in A201739a]
A201820b=[(i*90)+23 for i in A201820a]
A196000b=[(i*90)+19 for i in A196000a]
A202115b=[(i*90)+17 for i in A202115a]
A201816b=[(i*90)+13 for i in A201816a]
A201804b=[(i*90)+11 for i in A201804a]
A202110b=[(i*90)+7 for i in A202110a]





print(A181732b) 
"""print(A202116b)
print(A196007b)
print(A202112b)
print(A201822b)
print(A195993b)
print(A202129b)
print(A201817b)
print(A202113b)
print(A202101b)
print(A202114b)
print(A201818b)
print(A201734b)
print(A202105b)
print(A202104b)
print(A198382b)
print(A201819b)
print(A201739b)
print(A201820b)
print(A196000b)
print(A202115b)
print(A201816b)
print(A201804b)
print(A202110b)
"""

print(len(A181732b)) 
print(len(A202116b))
print(len(A196007b))
print(len(A202112b))
print(len(A201822b))
print(len(A195993b))
print(len(A202129b))
print(len(A201817b))
print(len(A202113b))
print(len(A202101b))
print(len(A202114b))
print(len(A201818b))
print(len(A201734b))
print(len(A202105b))
print(len(A202104b))
print(len(A198382b))
print(len(A201819b))
print(len(A201739b))
print(len(A201820b))
print(len(A196000b))
print(len(A202115b))
print(len(A201816b))
print(len(A201804b))
print(len(A202110b))


#print(len(A181732b) + len(A202116b) + len(A196007b) + len(A202112b) + len(A201822b) + len(A195993b) + len(A202129b) + len(A201817b) + len(A202113b) + len(A202101b) + len(A202114b) + len(A201818b) + len(A201734b) + len(A202105b) + len(A202104b) + len(A198382b) + len(A201819b) + len(A201739b) + len(A201820b) + len(A196000b) + len(A202115b) + len(A201816b) + len(A201804b) + len(A202110b))

newlist = A181732b + A202116b + A196007b + A202112b + A201822b + A195993b + A202129b + A201817b + A202113b + A202101b + A202114b + A201818b + A201734b + A202105b + A202104b + A198382b + A201819b + A201739b + A201820b + A196000b + A202115b + A201816b + A201804b + A202110b
#print("This is new list", sorted(newlist))
print(len(newlist)+2)
list_data = []


#del primeOmega[-10:]
#del primeTrue[-10:]
#print(primeOmega[-100:])
#print(primeTrue[-100:])
base10lim = (limit*90)+11
#primecount = primeOmega.count(0)#int(sum(primeTrue)) #this is possibly computationally more expensive than alternative solutions

#omegacount = int(sum(primeOmega))




#A201804 = [i for i,x in enumerate(primeOmega) if x == 0]
#print("This is part of A201804, the last 100 primes beneath the limit", A201804)#[-100:])
#A201804a = [(i*90)+11 for i in A201804]
#print("These are last 100 base-10 primes converted from A201804", A201804a[-100:], "at the limit of", base10lim)

#a_var = primecount/limit
#b_var = omegacount/limit
#c_var = omegacount/primecount
#d_var = primecount/omegacount
#e_var = primecount/base10lim#base10lim/primecount
#f_var = limit/base10lim
#g_var = omegacount/base10lim 


#list_data.append(primecount) #number of primes
#list_data.append(limit)      #the limit
#list_data.append(omegacount) #number of print operations == composite rows with print = +1 ~= number of factors (non-unique, that is total number)
#list_data.append(a_var)      #primes divided by the limit
#list_data.append(b_var)      #number of print operations divided by the limit
#list_data.append(c_var)      #number of print operations divided by the number of primes
#list_data.append(d_var)      #number of primes divided by nummber of print operations   
#list_data.append(base10lim)  #limit when mapped to a base-10 value
#list_data.append(e_var)
#list_data.append(f_var)
#list_data.append(g_var)

list_data.append(len(A181732a))# =[i for i,x in enumerate(A181732) if x == 0]
list_data.append(len(A202116a))#=[i for i,x in enumerate(A202116) if x == 0]
list_data.append(len(A196007a))#=[i for i,x in enumerate(A196007) if x == 0]
list_data.append(len(A202112a))#=[i for i,x in enumerate(A202112) if x == 0]
list_data.append(len(A201822a))#=[i for i,x in enumerate(A201822) if x == 0)]
list_data.append(len(A195993a))#=[i for i,x in enumerate(A195993) if x == 0]
list_data.append(len(A202129a))#=[i for i,x in enumerate(A202129) if x == 0]
list_data.append(len(A201817a))#=[i for i,x in enumerate(A201817) if x == 0)]
list_data.append(len(A202113a))#=[i for i,x in enumerate(A202113) if x == 0]
list_data.append(len(A202101a))#=[i for i,x in enumerate(A202101) if x == 0]
list_data.append(len(A202114a))#=[i for i,x in enumerate(A202114) if x == 0]
list_data.append(len(A201818a))#=[i for i,x in enumerate(A201818) if x == 0]
list_data.append(len(A201734a))#=[i for i,x in enumerate(A201734) if x == 0]
list_data.append(len(A202105a))#=[i for i,x in enumerate(A202105) if x == 0]
list_data.append(len(A202104a))#=[i for i,x in enumerate(A202104) if x == 0]
list_data.append(len(A198382a))#=[i for i,x in enumerate(A198382) if x == 0]
list_data.append(len(A201819a))#=[i for i,x in enumerate(A201819) if x == 0]
list_data.append(len(A201739a))#=[i for i,x in enumerate(A201739) if x == 0]
list_data.append(len(A201820a))#=[i for i,x in enumerate(A201820) if x == 0]
list_data.append(len(A196000a))#=[i for i,x in enumerate(A196000) if x == 0]
list_data.append(len(A202115a))#=[i for i,x in enumerate(A202115) if x == 0]
list_data.append(len(A201816a))#=[i for i,x in enumerate(A201816) if x == 0]
list_data.append(len(A201804a))#=[i for i,x in enumerate(A201804) if x == 0]
list_data.append(len(A202110a))#=[i for i,x in enumerate(A202110) if x == 0]

