#!/usr/bin/env python
import math
import cmath
from collections import Counter
import matplotlib.pyplot as plt 

"""
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

#here comes a function for generating composites
def drLD(x, l, m, z, o):   

  y = 90*(x*x) - l*x + m 
  if start <= y < limit: 
    primes[y-start] = primes[y-start]+1
    print("added y", y)
 
  p = z+(90*(x-1))
  newp_start = int(((start-y)/p))
  newp_lim = int(((limit-y)/p)+1)

  for n in range(newp_start, newp_lim):
  #  s = s+1
    new_y = y+(p*n)
    if start <= new_y < limit: 
      primes[new_y - start] = primes[new_y-start]+1

  q = o+(90*(x-1))
  newq_start = int(((start-y)/q))
  newq_lim = int(((limit-y)/q)+1)

  for n in range(newq_start, newq_lim):
  #  s = s+1
    new_y = y+(q*n)
    if start <= new_y < limit: 
      primes[new_y - start] = primes[new_y-start]+1


for x in range(1, int(new_limit.real)): # 10000 = 12; 100000 = 36; 1,000,000 = 108; 10,000,000 = 336; 100,000,000 = 1056; 1,000,000,000 = "Hey I need to checksum these tables, all hand-entered
 
#11
    drLD(x, 78, -1, 11, 91)  #11,91 @11, 203 5    564
    drLD(x, 120, 34, 7, 53)  #7,53  @4,  154 1    831
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

#13
#    drLD(x, 76, -1, 13, 91)   #13,91
#    drLD(x, 94, 18, 19, 67)  #19,67
#    drLD(x, 94, 24, 37, 49)  #37,49
#    drLD(x, 76, 11, 31, 73)  #31,73
#    drLD(x, 86, 6, 11, 83)   #11,83
#    drLD(x, 104, 29, 29, 47) #29,47
#    drLD(x, 86, 14, 23, 71)  #23,71
#    drLD(x, 86, 20, 41, 53)  #41,53
#    drLD(x, 104, 25, 17, 59) #17,59
#    drLD(x, 14, 0, 77, 89)   #77,89
#    drLD(x, 94, 10, 7, 79)   #7,79
#    drLD(x, 76, 15, 43, 61)  #43,61





#primes.remove(primes[0]) #delete the first element as it is not coded/operated on
#del primes[-100:]               #we delete the last 10 terms because they were there as "padding"
#print(primes)
plt.plot(primes)
plt.show()
A201804c = [i for i,x in enumerate(primes) if x == 0]
newA = [(i+(start)) for i in A201804c]

print(newA)
print("This is the number of A201804 primes", len(newA), "between", start, "and", limit)
A201804b = [(i*90)+11 for i in newA]

print("This is the base-10 expression of A201804 (see: A142317)", A201804b)#[-50:])
base10lim = (limit*90)+11
operators = int(new_limit.real)*12
print("This is the number of quadratic addresses", int(new_limit.real)*12)


print("")
print("This is the base-10 limit                                    :", base10lim)
#print("This is the span of addresses re:A201804 to be sieved        :", start, limit, "width:", (limit-start))
#print("This is ycount quadratic sequence equals an address in span  :", ycount)
#print("This is the smaller of p*q has an address in the span        :", pcount)
#print("This is the larger of p*q has an address in the span         :", qcount)
#print("This is the number of FREQUENCY OPERATORS/quadratic sequences:", operators)
print("This is the TOTAL AMPLITUDE for the addresses in the span    :", sum(primes))
#print("This is the number of EVALUATIONS performed by the algorithm :", int(s))#sum(evals))
print("This is the square root of the base10limit                   :", math.sqrt(base10lim))
#print("This is the math.sqrt(base10lim)/quadratric sequences / FO   :", math.sqrt(base10lim)/operators)
#print("This is the math.sqrt(base10lim)/EVALUATIONS by the algorithm:", math.sqrt(base10lim)/int(s))#sum(evals))
#print("This is the ratio sqrt(lim) to ACTUAL list ops               :", math.sqrt(base10lim)/sum(primes))
#print("Algorithm operations divided by FREQUENCY OPERATORS in span  :", float(int(s))/operators)
#print("Algorithm operations divided by TOTAL AMPLITUDE in span      :", float(int(s))/sum(primes))
#print("Evals divided by operators:", float(sum(evals))/operators)
#print("Evals divided by Operations:", float(sum(evals))/sum(primes))
#print("This is the base10limit divided by the number of operators   :", base10lim/operators)
"""
width = [8881, 35761, 80641, 143521, 224401, 323281, 440161, 575041, 727921, 898801, 1087681, 1294561, 1519441, 1762321, 2023201, 2302081, 2598961, 2913841, 3246721, 3597601]
primes1 = [756, 2483, 4970, 8292, 12223, 16689, 21664, 27500, 33737, 40571, 47992, 55974, 64580, 73607, 83184, 93274, 103825, 114935, 126731, 138835]
primes2 = [756, 1727, 2487, 3322, 3931, 4466, 4975, 5836, 6237, 6834, 7421, 7982, 8606, 9027, 9577, 10090, 10551, 11110, 11796, 12104]
#plt.plot(width)
plt.plot(primes1)
plt.plot(primes2)
plt.plot(primes1, "o")
plt.plot(primes2, "x")
plt.show()