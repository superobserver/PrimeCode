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
A224854 = [0]*int(limit+100) #(11,13)
def drLD(x, l, m, z, listvar, primitive): 
  "This is a composite generating function"
  y = 90*(x*x) - l*x + m
  listvar[y] = listvar[y]+1   
  p = z+(90*(x-1))
  for n in range (1, int(((limit-y)/p)+1)):  
    listvar[y+(p*n)] = listvar[y+(p*n)]+1

for x in range(1, int(new_limit.real)):


#11
    drLD(x, 120, 34, 7,  A224854, 11)
    drLD(x, 120, 34, 53, A224854, 11)



    drLD(x, 132, 48, 19, A224854, 11)
    drLD(x, 132, 48, 29, A224854, 11)

    
    drLD(x, 120, 38, 17, A224854, 11)
    drLD(x, 120, 38, 43, A224854, 11)


    drLD(x, 90, 11, 13, A224854, 11)
    drLD(x, 90, 11, 77, A224854, 11)


    drLD(x, 78, -1, 11, A224854, 11)
    drLD(x, 78, -1, 91, A224854, 11)


    drLD(x, 108, 32, 31, A224854, 11)
    drLD(x, 108, 32, 41, A224854, 11)


    drLD(x, 90, 17, 23, A224854, 11)
    drLD(x, 90, 17, 67, A224854, 11)


    drLD(x, 72, 14, 49, A224854, 11)
    drLD(x, 72, 14, 59, A224854, 11)


    drLD(x, 60, 4, 37, A224854, 11)
    drLD(x, 60, 4, 83, A224854, 11)


    drLD(x, 60, 8, 47, A224854, 11)
    drLD(x, 60, 8, 73, A224854, 11)


    drLD(x, 48, 6, 61, A224854, 11)
    drLD(x, 48, 6, 71, A224854, 11)


    drLD(x, 12, 0, 79, A224854, 11)
    drLD(x, 12, 0, 89, A224854, 11)


"""


# 19
    drLD(x, 70, -1, 19, 91, A224854, 19) #19,91
    drLD(x, 106, 31, 37, 37, A224854, 19) #37,73
    drLD(x, 34, 3, 73, 73, A224854, 19) #73,73
    drLD(x, 110, 27, 11, 59, A224854, 19) #11,59
    drLD(x, 110, 33, 29, 41, A224854, 19) #29,41
    drLD(x, 56, 6, 47, 77, A224854, 19) #47,77
    drLD(x, 74, 5, 23, 83, A224854, 19) #23,83
    drLD(x, 124, 40, 13, 43, A224854, 19) #13,43
    drLD(x, 70, 7, 31, 79, A224854, 19) #31,79
    drLD(x, 70, 13, 49, 61, A224854, 19) #49,61
    drLD(x, 106, 21, 7, 67, A224854, 19) #7,67
    drLD(x, 20, 0, 71, 89, A224854, 19) #71,89
    drLD(x, 74, 15, 53, 53, A224854, 19) #53,53
    drLD(x, 146, 59, 17, 17, A224854, 19) #17,17




#13
    drLD(x, 76, -1, 13, A224854, 13)
    drLD(x, 76, -1, 91, A224854, 13)#

    drLD(x, 94, 18, 19, A224854, 13)
    drLD(x, 94, 18, 67, A224854, 13)


    drLD(x, 94, 24, 37, A224854, 13)
    drLD(x, 94, 24, 49, A224854, 13)


    drLD(x, 76, 11, 31, A224854, 13)
    drLD(x, 76, 11, 73, A224854, 13)


    drLD(x, 86, 6, 11, A224854, 13)
    drLD(x, 86, 6, 83, A224854, 13)


    drLD(x, 104, 29, 29, A224854, 13)
    drLD(x, 104, 29, 47, A224854, 13)


    drLD(x, 86, 14, 23, A224854, 13)
    drLD(x, 86, 14, 71, A224854, 13)


    drLD(x, 86, 20, 41, A224854, 13)
    drLD(x, 86, 20, 53, A224854, 13)


    drLD(x, 104, 25, 17, A224854, 13)
    drLD(x, 104, 25, 59, A224854, 13)


    drLD(x, 14, 0, 77, A224854, 13)
    drLD(x, 14, 0, 89, A224854, 13)


    drLD(x, 94, 10, 7, A224854, 13)
    drLD(x, 94, 10, 79, A224854, 13)


    drLD(x, 76, 15, 43, A224854, 13)
    drLD(x, 76, 15, 61, A224854, 13)

"""


A224854 = A224854[:-100] #this list contains the amplitude data
A224854a = [i for i,x in enumerate(A224854) if x == 0] #this is the "address value" for twin prime valued addresses
print(A224854a, "This is A224854")
new = [(i*90)+11 for i in A224854a] #this is the smallest member of a twin prime pair for 11,13
#print(new)
print(len(A224854a))

#11
 #   drLD(x, 120, 34, 7, 53, A224854, 11)
 #   drLD(x, 132, 48, 19, 29, A224854, 11)
 #   drLD(x, 120, 38, 17, 43, A224854, 11)
 #   drLD(x, 90, 11, 13, 77, A224854, 11)
 #   drLD(x, 78, -1, 11, 91, A224854, 11)
 #   drLD(x, 108, 32, 31, 41, A224854, 11)
 #   drLD(x, 90, 17, 23, 67, A224854, 11)
 #   drLD(x, 72, 14, 49, 59, A224854, 11)
 #   drLD(x, 60, 4, 37, 83, A224854, 11)
 #   drLD(x, 60, 8, 47, 73, A224854, 11)
 #   drLD(x, 48, 6, 61, 71, A224854, 11)
 #   drLD(x, 12, 0, 79, 89, A224854, 11)
#13
  #  drLD(x, 76, -1, 13, 91, A224854, 13)
  #  drLD(x, 94, 18, 19, 67, A224854, 13)
  #  drLD(x, 94, 24, 37, 49, A224854, 13)
  #  drLD(x, 76, 11, 31, 73, A224854, 13)
  #  drLD(x, 86, 6, 11, 83, A224854, 13)
  #  drLD(x, 104, 29, 29, 47, A224854, 13)
  #  drLD(x, 86, 14, 23, 71, A224854, 13)
  #  drLD(x, 86, 20, 41, 53, A224854, 13)
  #  drLD(x, 104, 25, 17, 59, A224854, 13)
  #  drLD(x, 14, 0, 77, 89, A224854, 13)
  #  drLD(x, 94, 10, 7, 79, A224854, 13)
  #  drLD(x, 76, 15, 43, 61, A224854, 13)
#A224854 = A224854[:-100]