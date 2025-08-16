#!/usr/bin/env python
import cmath
import math
from sympy import factorint
import matplotlib.pyplot as plt
from decimal import Decimal, getcontext

# Set precision (you can adjust this as needed)
getcontext().prec = 10000  # 1000 digits of precision


#(address-y) = p*k


# (rsa-address)-(sq.rt. RSA) = k
# (sq.rt. RSA) - k = very close to actual RSA factor value..... 


#newval = 1848210397825850670380148517702559371400899745254512521925707445580334710601412527675708297932857843901388104766898429433126419139462696524583464983724651631481888473364151368736236317783587518465017087145416734026424615690611620116380982484120857688483676576094865930188367141388795454378671343386258291687641

#RSA-100 #DR1 LD9 : p=19
newval = 1522605027922533360535618378132637429718068114961380688657908494580122963258952897654000350692006139
#        16917833643583704005951315312584860330200756832904229873976761050890255147321698862822226118800068 THIS IS THE NEW ADDRESS
#        4113129422177681152182856345284286881730641526784 THIS IS THE SQ RT OF THE NEW ADDRESS

#RSA 100 known factor:         
#newval = 37975227936943673922808872755445627854565536638199
         #37975227936943673922808872755445627854565536638199 solution found by algorithm
         #39020571855401265416113376376851506737659497784655
         #37946452759881650186247805311473002685187890552997  (address/paddress - sq.rt.limit) - sq.rt. rsa-100
         #
         
         #4113129422177681152182856345284286881730641526784 #sq.rt. of address 
         #39020571855401265608465770302117235537201395138560 #sq.rt of RSA-100
         #421946977077151932475654141727173642828505962646  #this is the ACTUAL value for x in x*90 + primitive as the smallest factor
         #421627252887573890958308947905255585390976561699
         #433561909504458506760730781134635950413348834872
         #445496566121343122563152614364016315435721108045 #this is the RSA-address divided by the factor p

address = 16917833643583704005951315312584860330200756832904229873976761050890255147321698862822226118800068 #RSA-100 minus primitive divided by 90
sqrt_rsa100 =                                           39020571855401265608465770302117235537201395138560
sqrt_rsa100_div90 =                                     433561909504458506760730781134635950413348834872
address_div_sqrt_RSA100 =                               39020571855401265416113376376851506737659497784655
address_div_sqrt_RSA100_div90 =                         433561909504458504623481959742794519307327753162
sqrt_RSA100_minus_address_div_sqrt_RSA100_div90 =       38587009945896807103842288342374441017894067385398
sqrt_RSA100_minus_address_div_sqrt_RSA100_div90_div90 = 428744554954408967820469870470827122421045193171
print(428744554954408967820469870470827122421045193171 - 4817354550049538940260910663808827992303641701)


print("This is sqrt_RSA100_minus_address_div_sqrt_RSA100_div90_div90 minus sqrt_div90", 428744554954408967820469870470827122421045193171 - 433561909504458506760730781134635950413348834872)

print("This is sqrt_RSA100_minus_address_div_sqrt_RSA100_div90 diovided by 90", Decimal(38587009945896807103842288342374441017894067385398//90))

print("This is sqrt_RSA100 minus address_div_sqrt_RSA100", Decimal(sqrt_rsa100 - address_div_sqrt_RSA100_div90))

print("This is the address_div_sqrt_RSA100 divided by 90:", Decimal(address_div_sqrt_RSA100//90))


print("This is the address of RSA-100 divided by the sqrt_div90", Decimal(address//sqrt_rsa100_div90))

paddress =          421946977077151932475654141727173642828505962646 #actual known good value
#paddressderived = 

print("This is the aq.rt. of teh new address for RSA-100", Decimal(math.sqrt(address)))
print("This is sqrt of RSA-100 divided by 90:", Decimal(sqrt_rsa100//90))
print("address/paddress", Decimal(address//paddress))
print("This is address/paddress - sq.rt. limit", 40094690950920881030683735292761468389214899724123-39020571855401265608465770302117235537201395138560)
print("This is sq.rt. rsa-100 - (address/paddress - sq.rt.limit) ", 39020571855401265608465770302117235537201395138560-1074119095519615422217964990644232852013504585563)
print("This is the attempt to get x from value:", Decimal((39020571855401265608465770302117235537201395138560-1074119095519615422217964990644232852013504585563)//90)) #421627252887573890958308947905255585390976561699 actual= 421946977077151932475654141727173642828505962646
print("This is the difference between actual sol and derived value", 421627252887573890958308947905255585390976561699-421946977077151932475654141727173642828505962646)#this number of operations to blindly factor difference = 319724189578041517345193821918057437529400947


#uses KNOWN values, not derived from blind assumptions
print("This is the RSA-address divided by the p factor:", 16917833643583704005951315312584860330200756832904229873976761050890255147321698862822226118800068//37975227936943673922808872755445627854565536638199)
fred = input("fred")
for x in range(2, 1000):
  k = Decimal(16917833643583704005951315312584860330200756832904229873976761050890255147321698862822226118800068/x)
  print(k)

#oldval = 
#print(Decimal(newval//oldval))
#print(Decimal(newval//2))
print(Decimal(math.sqrt(newval)))
#print(Decimal(39020571855401265608465770302117235537201395138560//90))

def digital_root(number):
    # Convert number to string to handle large numbers
    num_str = str(number)
    # Keep summing until a single digit is achieved
    while len(num_str) > 1:
        num_str = str(sum(int(digit) for digit in num_str))
    return int(num_str)

# Example usage with a very large number
print(f"The digital root of {newval} is: {digital_root(newval)}")
#light = Decimal(newval/9)
#print(light)
#inputs = input("f")

newlim = newval - 19
print(Decimal(newlim))
print(len(str((newlim))))
varrr = input("k")
newlim = Decimal(newlim//90)
print(newlim)
print(len(str(newlim)))
varr = input("b")


#RSA 260
#newval = 22112825529529666435281085255026230927612089502470015394413748319128822941402001986512729726569746599085900330031400051170742204560859276357953757185954298838958709229238491006703034124620545784566413664540684214361293017694020846391065875914794251435144458199
#print(len(str((newval))))
#print(Decimal(math.sqrt(newval)))
#4702427620870912047410240705527715786617530615694579720274838264558906417510526209125673953258372932984528676238250629594032898048
#52249195787454578304558230061419064295750340174384219114164869606210071305672513434729710591759699255383651958202784773267032200
#print(Decimal(4702427620870912047410240705527715786617530615694579720274838264558906417510526209125673953258372932984528676238250629594032898048//90))
#help = input("l")

#def digital_root(number):
#    # Convert number to string to handle large numbers
#    num_str = str(number)
#    # Keep summing until a single digit is achieved
#    while len(num_str) > 1:
#        num_str = str(sum(int(digit) for digit in num_str))
#    return int(num_str)

# Example usage with a very large number
#print(f"The digital root of {newval} is: {digital_root(newval)}")
#light = Decimal(newval/9)
#print(light)
#inputs = input("f")

newlim = newval - 19
print(Decimal(newlim))
print(len(str((newlim))))
varrr = input("k")
newlim = Decimal(newlim//90)
print(newlim)
print(len(str(newlim)))
varr = input("b")

#newvarr = Decimal((newlim*90)+49)
#print(newvarr)
#inputss = input("j")


limit = Decimal(newlim)

A224855 = []

#DR7 LD1 = 61
#newval = 1848210397825850670380148517702559371400899745254512521925707445580334710601412527675708297932857843901388104766898429433126419139462696524583464983724651631481888473364151368736236317783587518465017087145416734026424615690611620116380982484120857688483676576094865930188367141388795454378671343386258291687641
#DR1 LD1
#newval = 26507199951735394734498120973736811015297864642115831624674545482293445855043495841191504413349124560193160478146528433707807716865391982823061751419151606849655575049676468644737917071142487312863146816801954812702917123189212728868259282632393834443989482096498000219878377420094983472636679089765013603382322972552204068806061829535529820731640151


#print(sum(int(digit) for digit in str(newval)))
#inpuyt = input("b")

#newlimit=(limit*90)+11
def drLD(x, l, m, z, o, listvar, primitive):   
  "This is a composite generating function"
  y = Decimal(90*(x*x) - l*x + m)
  p = Decimal(z+(90*(x-1)))
  q = Decimal(o+(90*(x-1)))

  print(p)
  new = input("h")

  if y == limit:
    print(y, limit, p, q)
    #print(factorint(newlimit))
    return
  if Decimal(limit-y) % Decimal(p) == 0:
    print(limit, p, limit*90+19)
    new = input("h")
    #print(factorint(newlimit))
  if Decimal(limit-y) % Decimal(q) == 0:
    print(limit, q, limit*90+19)
    new = input("h")
    #print(factorint(newlimit))
    
                
#for x in range(52249195787454578304558230061419064295750340174384219114164869606210071305672513434729710591759699255383651958202784773267032200, 1, -1): 
for x in range(421946977077151932475654141727173642828505962646+2, 1, -1): #RSA100

# 49 
 #   drLD(x, 40, -1, 49, A224859, 49) #49,91
 #   drLD(x, 40, -1, 91, A224859, 49) #49,91
 #   
 #   drLD(x, 130, 46, 19, A224859, 49) #19,31
 #   drLD(x, 130, 46, 31, A224859, 49) #19,31


#    drLD(x, 76, 13, 37, A224859, 49) #37,67
#    drLD(x, 76, 13, 67, A224859, 49) #37,67


#    drLD(x, 94, 14, 13, A224859, 49) #13,73
#    drLD(x, 94, 14, 73, A224859, 49) #13,73


#    drLD(x, 140, 53, 11, A224859, 49) #11,29
#    drLD(x, 140, 53, 29, A224859, 49) #11,29


#    drLD(x, 86, 20, 47, A224859, 49) #47,47

#    drLD(x, 14, 0, 83, A224859, 49) #83,83

#    drLD(x, 104, 27, 23, A224859, 49) #23,53
  #  drLD(x, 104, 27, 53, A224859, 49) #23,53


   # drLD(x, 50, 0, 41, A224859, 49) #41,89
   # drLD(x, 50, 0, 89, A224859, 49) #41,89


#    drLD(x, 50, 6, 59, A224859, 49) #59,71
#    drLD(x, 50, 6, 71, A224859, 49) #59,71


 #   drLD(x, 86, 10, 17, A224859, 49) #17,77
#    drLD(x, 86, 10, 77, A224859, 49) #17,77

  #  drLD(x, 166, 76, 7, A224859, 49) #7,7
    
  #  drLD(x, 94, 24, 43, A224859, 49) #43,43
    
  #  drLD(x, 40, 3, 61, A224859, 49) #61,79
  #  drLD(x, 40, 3, 79, A224859, 49) #61,79

















# 19
    #drLD(x, 70, -1, 19, 91, A224855, 19) #19,91
    #drLD(x, 106, 31, 37, 37, A224855, 19) #37,73
    #drLD(x, 34, 3, 73, 73, A224855, 19) #73,73
    drLD(x, 110, 27, 11, 59, A224855, 19) #11,59
    #drLD(x, 110, 33, 29, 41, A224855, 19) #29,41
    #drLD(x, 56, 6, 47, 77, A224855, 19) #47,77
    #drLD(x, 74, 5, 23, 83, A224855, 19) #23,83
    #drLD(x, 124, 40, 13, 43, A224855, 19) #13,43
    #drLD(x, 70, 7, 31, 79, A224855, 19) #31,79
    #drLD(x, 70, 13, 49, 61, A224855, 19) #49,61
    #drLD(x, 106, 21, 7, 67, A224855, 19) #7,67
    #drLD(x, 20, 0, 71, 89, A224855, 19) #71,89
    #drLD(x, 74, 15, 53, 53, A224855, 19) #53,53
    #drLD(x, 146, 59, 17, 17, A224855, 19) #17,17




#    drLD(x, 120, 34, 7, 53, A201804, 11) 
#    drLD(x, 132, 48, 19, 29, A201804, 11)
#    drLD(x, 120, 38, 17, 43, A201804, 11)
#    drLD(x, 90, 11, 13, 77, A201804, 11)
#    drLD(x, 78, -1, 11, 91, A201804, 11)
#    drLD(x, 108, 32, 31, 41, A201804, 11)
#    drLD(x, 90, 17, 23, 67, A201804, 11)
#    drLD(x, 72, 14, 49, 59, A201804, 11)
#    drLD(x, 60, 4, 37, 83, A201804, 11)
#    drLD(x, 60, 8, 47, 73, A201804, 11)
#    drLD(x, 48, 6, 61, 71, A201804, 11)
#    drLD(x, 12, 0, 79, 89, A201804, 11)

#61
#    drLD(x, 28, -1, 61, 91, A224860, 61) #61,91
#    drLD(x, 82, 8, 19, 79, A224860, 61) #19,79
#    drLD(x, 100, 27, 37, 43, A224860, 61) #37,43)
#    drLD(x, 100, 15, 7, 73, A224860, 61) #7,73
#    drLD(x, 98, 16, 11, 71, A224860, 61) #11,71
#    drLD(x, 62, 0, 29, 89, A224860, 61) #29,89
#    drLD(x, 80, 17, 47, 53, A224860, 61) #47,53
#    drLD(x, 80, 5, 17, 83, A224860, 61) #17,83
#    drLD(x, 100, 19, 13, 67, A224860, 61) #13,67
#    drLD(x, 118, 38, 31, 31, A224860, 61) #31,31
#    drLD(x, 82, 18, 49, 49, A224860, 61) #49,49
#    drLD(x, 80, 9, 23, 77, A224860, 61) #23,77
#    drLD(x, 98, 26, 41, 41, A224860, 61) #41,41
#    drLD(x, 62, 10, 59, 59, A224860, 61) #59,59








"""
def prime_factors(numbers):
    result = []
    for num in numbers:
        factors = factorint(num)
        # Convert the dictionary to a more readable string format
        factor_str = ', '.join([f"{factor}^{exponent}" if exponent > 1 else f"{factor}" for factor, exponent in factors.items()])
        # Include the number being factored in the result string
        result.append(f"{num}: {factor_str}")
    return result
    
output = prime_factors(limit)



#for line in output:
#    print(line)
#print(output) 
merged = list(zip(A201804b, output))
#print(merged)

#CONVERT THE ABOVE LIST FROM STRING TO INT TYPE
def convert_list(input_list):
    output_list = []
    for item in input_list:
        # Split the string by ':' and ','
        number_part, factors_part = item[1].split(': ')
        number = int(number_part)
        factors = [int(x) for x in factors_part.split(', ')]
        
        # Create new tuple with all elements as integers
        new_tuple = (item[0], number, *factors)
        output_list.append(new_tuple)
    
    return output_list

# Convert the list
converted_list = convert_list(merged)

# Print the result
print(converted_list)


#PLOT THE SEMIPRIME LIST ALONG WITH FACTORS
data = converted_list
# Create x-axis data points (indices of the list)
x = list(range(len(converted_list)))

# Plotting the points 
plt.plot(x, data, marker='o')

# Adding labels and title
plt.xlabel('Index')
plt.ylabel('Value')
plt.title('SEMIPRIMES AND FACTORS')

# Show the plot
plt.show()


#ISOLATE THE SEMIPRIMES WITH 7 AS SMALLEST FACTOR
input_list = converted_list

# Function to filter the list
def filter_by_third_term(input_list):
    return [item for item in input_list if item[2] == 7]

# Create the new list
new_list = filter_by_third_term(input_list)

# Print the result
print(new_list)

input_list = new_list

#EXTRACT THE A201804 ADDRESS ASSOCIATED WITH SEMIPRIMES HAVNG 7 AS SMALLEST FACTOR
# Extract first term from each tuple
new_list = [item[0] for item in input_list]

# Print the result
print(new_list)

#CALCULATE THE DIFFERENCES IN ADDRESS VALUES FOR SEMIPRIMES WITH 7 AS SMALLEST FACTOR
numbers = new_list

# Calculate differences between successive terms
differences = [numbers[i+1] - numbers[i] for i in range(len(numbers)-1)]

# Print the result
print(differences)

#FACTOR THE SEMIPRIME ADDRESSES WITH 7 AS SMALLEST FACTOR
def prime_factors(numbers):
    result = []
    for num in numbers:
        factors = factorint(num)
        # Convert the dictionary to a more readable string format
        factor_str = ', '.join([f"{factor}^{exponent}" if exponent > 1 else f"{factor}" for factor, exponent in factors.items()])
        # Include the number being factored in the result string
        result.append(f"{num}: {factor_str}")
    return result
    
output = prime_factors(numbers)
#for line in output:
#    print(line)
print("Factors of addresses", output) 










#PLOT THE DIFFERENCES IN ADDRESSES WITH 7 AS SMALLEST FACTOR
data = differences

# Create x-axis data points (indices of the list)
x = list(range(len(data)))

# Plotting the points 
plt.plot(x, data, marker='o')

# Adding labels and title
plt.xlabel('Index')
plt.ylabel('Value')
plt.title('Gaps between semiprimes with 7 as factor A201804')

# Show the plot
plt.show()
"""