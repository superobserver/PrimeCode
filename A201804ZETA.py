#!/usr/bin/env python
import cmath
import math
#limit = 20
limit = input("number")
limit = int(limit)
h = limit
epoch = 90*(h*h) - 12*h + 1
limit = epoch
print(limit)
a = 90
b = -300
c = 250 - limit 
d = (b**2) - (4*a*c)
sol1 = (-b-cmath.sqrt(d))/(2*a)
sol2 = (-b+cmath.sqrt(d))/(2*a)
new_limit = sol2
print(new_limit)
A201804 = [0]*int(limit+100) #(11,13)

yforseven = []
def drLD(x, l, m, z, o, listvar, primitive): 
  "This is a composite generating function"
  y = 90*(x*x) - l*x + m

  listvar[y] = listvar[y]+1   
  p = z+(90*(x-1))
  q = o+(90*(x-1))

  for n in range (1, int(((limit-y)/p)+1)):  
    listvar[y+(p*n)] = listvar[y+(p*n)]+1
  for n in range (1, int(((limit-y)/q)+1)):  
    listvar[y+(q*n)] = listvar[y+(q*n)]+1



for x in range(1, int(new_limit.real)):
#11
#11
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
    
print(A201804)
A201804 = A201804[:-100] #this list contains the amplitude data
A201804a = [i for i,x in enumerate(A201804) if x == 0] #this is the "address value" for twin prime valued addresses
A201804b = [i for i,x in enumerate(A201804) if x > 0] #this is the "address value" for twin prime valued addresses
print("Number of primes beneath limit", len(A201804), len(A201804a))
print(A201804a, "This is A201804 Hole addresses")
new = [(i*90)+11 for i in A201804a] #this is the smallest member of a twin prime pair for 11,13
print(new)
print("This is the primes", len(A201804a))
"""
    drLD(x, 120, 34, 7,  A201804, 11)
    drLD(x, 120, 34, 53, A201804, 11)



    drLD(x, 132, 48, 19, A201804, 11)
    drLD(x, 132, 48, 29, A201804, 11)

    
    drLD(x, 120, 38, 17, A201804, 11)
    drLD(x, 120, 38, 43, A201804, 11)


    drLD(x, 90, 11, 13, A201804, 11)
    drLD(x, 90, 11, 77, A201804, 11)


    drLD(x, 78, -1, 11, A201804, 11)
    drLD(x, 78, -1, 91, A201804, 11)


    drLD(x, 108, 32, 31, A201804, 11)
    drLD(x, 108, 32, 41, A201804, 11)


    drLD(x, 90, 17, 23, A201804, 11)
    drLD(x, 90, 17, 67, A201804, 11)


    drLD(x, 72, 14, 49, A201804, 11)
    drLD(x, 72, 14, 59, A201804, 11)


    drLD(x, 60, 4, 37, A201804, 11)
    drLD(x, 60, 4, 83, A201804, 11)


    drLD(x, 60, 8, 47, A201804, 11)
    drLD(x, 60, 8, 73, A201804, 11)


    drLD(x, 48, 6, 61, A201804, 11)
    drLD(x, 48, 6, 71, A201804, 11)


    drLD(x, 12, 0, 79, A201804, 11)
    drLD(x, 12, 0, 89, A201804, 11)
	
	
print(A201804)
A201804 = A201804[:-100] #this list contains the amplitude data
A201804a = [i for i,x in enumerate(A201804) if x == 0] #this is the "address value" for twin prime valued addresses
A201804b = [i for i,x in enumerate(A201804) if x > 0] #this is the "address value" for twin prime valued addresses
print("Number of primes beneath limit", len(A201804), len(A201804a))
print(A201804a, "This is A201804 Hole addresses")
new = [(i*90)+11 for i in A201804a] #this is the smallest member of a twin prime pair for 11,13
print(new)
print("This is the primes", len(A201804a))
#print("This is composites", len(A201804b))
#print(yforseven)




   <120, 34, 7>
   <120, 34, 53>
   <132, 48, 19>
   <132, 48, 29>

    
    <120, 38, 17>
    <120, 38, 43>


    <90, 11, 13>
    <90, 11, 77>


    <78, -1, 11>
    <78, -1, 91>


    <108, 32, 31>
    <108, 32, 41>


    <90, 17, 23>
    <90, 17, 67>


    <72, 14, 49>
    <72, 14, 59>


    <60, 4, 37>
    <60, 4, 83>


    <60, 8, 47>
    <60, 8, 73>


    <48, 6, 61>
    <48, 6, 71>


    <12, 0, 79>
    <12, 0, 89>
	"""