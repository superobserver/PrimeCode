import csv
from collections import Counter
from matplotlib import pyplot as plt

csv_file_path1 = 'A224854.csv'
csv_file_path2 = 'A224855.csv'
csv_file_path3 = 'A224856.csv'
csv_file_path4 = 'A224857.csv'
csv_file_path5 = 'A224859.csv'
csv_file_path6 = 'A224860.csv'
csv_file_path7 = 'A224862.csv'
csv_file_path8 = 'A224864.csv'
csv_file_path9 = 'A224865.csv'



data_list = []
with open(csv_file_path1, 'r') as file:
    csv_reader = csv.reader(file)
#    data_list = []
    for line in csv_reader:
        data_list.append([int(x) for x in line])
with open(csv_file_path2, 'r') as file:
    csv_reader = csv.reader(file)
#    data_list = []
    for line in csv_reader:
        data_list.append([int(x) for x in line])
with open(csv_file_path3, 'r') as file:
    csv_reader = csv.reader(file)
#    data_list = []
    for line in csv_reader:
        data_list.append([int(x) for x in line])
with open(csv_file_path4, 'r') as file:
    csv_reader = csv.reader(file)
#    data_list = []
    for line in csv_reader:
        data_list.append([int(x) for x in line])
with open(csv_file_path5, 'r') as file:
    csv_reader = csv.reader(file)
#    data_list = []
    for line in csv_reader:
        data_list.append([int(x) for x in line])
with open(csv_file_path6, 'r') as file:
    csv_reader = csv.reader(file)
#    data_list = []
    for line in csv_reader:
        data_list.append([int(x) for x in line])
with open(csv_file_path7, 'r') as file:
    csv_reader = csv.reader(file)
#    data_list = []
    for line in csv_reader:
        data_list.append([int(x) for x in line])
with open(csv_file_path8, 'r') as file:
    csv_reader = csv.reader(file)
#    data_list = []
    for line in csv_reader:
        data_list.append([int(x) for x in line])
with open(csv_file_path9, 'r') as file:
    csv_reader = csv.reader(file)
#    data_list = []
    for line in csv_reader:
        data_list.append([int(x) for x in line])

		


#print(data_list)
single_list = [item for sublist in data_list for item in sublist]
#print(single_list)

plt.title("This is the aggregate data")
plt.plot(single_list, "o")
plt.show()

flat_list = []
for x in single_list:
    flat_list.append(x)
#print(flat_list)
print(Counter(flat_list))
print(sum(flat_list))
#newlist = [(i*90)+11 for i in flat_list]
#plt.plot(newlist, "x")
#plt.show()
#print(Counter(newlist))




