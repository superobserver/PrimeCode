#!/usr/bin/env python
import csv
import math
import cmath
import sys

#start = int(sys.argv[1])
#import multiprocessing
#print("Number of cpu : ", multiprocessing.cpu_count())

#start = input("start value here:")
start =  99999999999999999 #works=99999999999999999 #broken=9999999999999999999 #999999999999999999000
                                      #99999999999999999
print("Our base-10 starting point:", (start*90+11))
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
  newp_start = int(((start-y)/p)-0)
  newp_lim = int(((limit-y)/p)+1)

  for n in range(newp_start, newp_lim):
  #  s = s+1
    new_y = y+(p*n)
    if start <= new_y < limit: 
      primes[new_y - start] = primes[new_y-start]+1

  q = o+(90*(x-1))
  newq_start = int(((start-y)/q)-0)
  newq_lim = int(((limit-y)/q)+1)

  for n in range(newq_start, newq_lim):
  #  s = s+1
    new_y = y+(q*n)
    if start <= new_y < limit: 
      primes[new_y - start] = primes[new_y-start]+1





for x in range(1, int(new_limit.real)): # 10000 = 12; 100000 = 36; 1,000,000 = 108; 10,000,000 = 336; 100,000,000 = 1056; 1,000,000,000 = "Hey I need to checksum these tables, all hand-entered

    drLD(x, 108, 32, 31, 41) #31,41 @14, 176 6    262
    
print(primes)
address = [i for i,x in enumerate(primes) if x == 0]
new_address = [(i+(start)) for i in address]
with open('31_41.csv', 'w', newline='') as file:
    # Step 4: Using csv.writer to write the list to the CSV file
    writer = csv.writer(file)
    writer.writerow(new_address) # Use writerow for single list

#close window
sys.exit()