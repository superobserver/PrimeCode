#!/usr/bin/env python
import cmath
import math
from sympy import factorint
import matplotlib.pyplot as plt


limit = input("give a number for the limit (that will be multiplied by 90x^2)")
limit = int(limit) 
h = limit
epoch = 90*(h*h) - 12*h + 1

limit = epoch
base10 = (limit*90)+11
a = 90
b = -300
c = 250 - limit 
d = (b**2) - (4*a*c)
sol1 = (-b-cmath.sqrt(d))/(2*a)
sol2 = (-b+cmath.sqrt(d))/(2*a)
new_limit = sol2

A201804 = [0]*int(limit+100) #(11,13)

def drLD(x, l, m, z, o, listvar, primitive):   
  "This is a composite generating function"
  y = 90*(x*x) - l*x + m
  A201804[y] = A201804[y]+1
  p = z+(90*(x-1))
  q = o+(90*(x-1))
  for n in range (1, int(((limit-y)/p)+1)):  
    listvar[y+(p*n)] = listvar[y+(p*n)]+1
  for n in range (1, int(((limit-y)/q)+1)):
    listvar[y+(q*n)] = listvar[y+(q*n)]+1

for x in range(1, int(new_limit.real)): 

    drLD(x, -2, 0, 91, 91, A201804, 91) #91,91
    drLD(x, 142, 56, 19, 19, A201804, 91) #19,19
    drLD(x, 70, 10, 37, 73, A201804, 91) #37, 73
    drLD(x, 128, 43, 11, 41, A201804, 91) #11, 41
    drLD(x, 92, 21, 29, 59, A201804, 91) #29,59
    drLD(x, 110, 32, 23, 47, A201804, 91) #23,47
    drLD(x, 20, 1, 77, 83, A201804, 91) #77,83
    drLD(x, 160, 71, 7, 13, A201804, 91) #7,13
    drLD(x, 88, 19, 31, 61, A201804, 91) #31,61
    drLD(x, 52, 5, 49, 79, A201804, 91) #49,79
    drLD(x, 70, 12, 43, 67, A201804, 91) #43,67
    drLD(x, 110, 30, 17, 53, A201804, 91) #17,53
    drLD(x, 38, 4, 71, 71, A201804, 91) #71,71
    drLD(x, 2, 0, 89, 89, A201804, 91) #89,89








A201804 = A201804[:-100]
new1 = A201804.count(0)
print(len(A201804))
print("Count of zero", new1)
print("epoch limit", limit)
A201804a = [i for i,x in enumerate(A201804) if x == 0]
A201804b = [i for i,x in enumerate(A201804) if x == 1]
A0 = [(i*90)+1 for i in A201804a]
print(A201804a, "The prime sequence OEIS A201804")
print(A201804b, "The complement to Oeis A201804") 
print("The primes such that 90*n+11 is prime", A0)
# Calculate differences between successive terms
#differences = [numbers[i+1] - numbers[i] for i in range(len(numbers)-1)]
# Print the result
#print(differences)
#print(A201804)

"""
    
    drLD(x, 72, -1, 17, 91, A201804, 17)   #17,91
    drLD(x, 108, 29, 19, 53, A201804, 17) #19,53
    drLD(x, 72, 11, 37, 71, A201804, 17)   #37,71
    drLD(x, 18, 0, 73, 89, A201804, 17)   #73,89
    drLD(x, 102, 20, 11, 67, A201804, 17)  #11,67
    drLD(x, 138, 52, 13, 29, A201804, 17) #13,29
    drLD(x, 102, 28, 31, 47, A201804, 17)  #31,47
    drLD(x, 48, 3, 49, 83, A201804, 17)  #49,83
    drLD(x, 78, 8, 23, 79, A201804, 17)  #23,79
    drLD(x, 132, 45, 7, 41, A201804, 17) #7,41
    drLD(x, 78, 16, 43, 59, A201804, 17)   #43,59
    drLD(x, 42, 4, 61, 77, A201804, 17) #61,77   

    drLD(x, 120, 34, 7, 53, A201804, 11) 
    drLD(x, 132, 48, 19, 29, A201804, 11)
    drLD(x, 120, 38, 17, 43, A201804, 11)
    drLD(x, 90, 11, 13, 77, A201804, 11)
    drLD(x, 78, -1, 11, 91, A201804, 11)
    drLD(x, 108, 32, 31, 41, A201804, 11)
    drLD(x, 90, 17, 23, 67, A201804, 11)
    drLD(x, 72, 14, 49, 59, A201804, 11)
    drLD(x, 60, 4, 37, 83, A201804, 11)
    drLD(x, 60, 8, 47, 73, A201804, 11)
    drLD(x, 48, 6, 61, 71, A201804, 11)
    drLD(x, 12, 0, 79, 89, A201804, 11)




#FACTOR THE SEMIPRIMES
def prime_factors(numbers):
    result = []
    for num in numbers:
        factors = factorint(num)
        # Convert the dictionary to a more readable string format
        factor_str = ', '.join([f"{factor}^{exponent}" if exponent > 1 else f"{factor}" for factor, exponent in factors.items()])
        # Include the number being factored in the result string
        result.append(f"{num}: {factor_str}")
    return result
    
output = prime_factors(A0)
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
    return [item for item in input_list if item[2] == 277]

# Create the new list
new_list = filter_by_third_term(input_list)

# Print the result
print("Should be the 7 list", new_list)

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
### stuff and tests stored here ######
"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# List of tuples
list_of_tuples = [(4, 371, 7, 53), (6, 551, 19, 29), (8, 731, 17, 43), (14, 1271, 31, 41)]

# Convert list of tuples to numpy array
X = np.array(list_of_tuples)

# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Perform PCA
pca = PCA()
X_pca = pca.fit_transform(X_scaled)

# Print the explained variance ratio for each principal component
print("Explained variance ratio:", pca.explained_variance_ratio_)

# Cumulative explained variance ratio
cumulative_variance_ratio = np.cumsum(pca.explained_variance_ratio_)
print("Cumulative explained variance ratio:", cumulative_variance_ratio)

# Visualize how much variance is explained by number of components
plt.figure(figsize=(10, 5))
plt.plot(range(1, len(pca.explained_variance_ratio_) + 1), cumulative_variance_ratio, 'bo-')
plt.xlabel('Number of Components')
plt.ylabel('Cumulative Explained Variance Ratio')
plt.title('Explained Variance by Number of Components')
plt.grid(True)
plt.show()

# Since we only have 4 features, we can visualize all PCs, but let's focus on the first 2 for simplicity
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# Visualize the transformed data points in 2D
plt.figure(figsize=(10, 5))
plt.scatter(X_pca[:, 0], X_pca[:, 1], alpha=0.5)
for i, (x, y) in enumerate(zip(X_pca[:, 0], X_pca[:, 1])):
    plt.text(x, y, f'data {i+1}', fontsize=9)
plt.xlabel('First Principal Component')
plt.ylabel('Second Principal Component')
plt.title('Data Points in PCA Space')
plt.axis('equal')
plt.show()

# Additional visualization: How original features contribute to each PC
plt.figure(figsize=(10, 5))
features = ['Feature 1', 'Feature 2', 'Feature 3', 'Feature 4']
for i, (x, y) in enumerate(zip(pca.components_[0], pca.components_[1])):
    plt.plot([0, x], [0, y], 'k-', lw=1, alpha=0.8)
    plt.text(x, y, features[i])
plt.plot([-0.7, 0.7], [0, 0], 'k--', lw=1)
plt.plot([0, 0], [-0.7, 0.7], 'k--', lw=1)
plt.xlim(-0.7, 0.7)
plt.ylim(-0.7, 0.7)
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.title('Feature Contributions to First Two PCs')
plt.axis('equal')
plt.show()





"""