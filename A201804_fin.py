import csv
from collections import Counter
from matplotlib import pyplot as plt

csv_file_path1 = '11_91.csv'
csv_file_path2 = '7_53.csv'
csv_file_path3 = '19_29.csv'
csv_file_path4 = '17_43.csv'
csv_file_path5 = '13_77.csv'
csv_file_path6 = '31_41.csv'
csv_file_path7 = '23_67.csv'
csv_file_path8 = '49_59.csv'
csv_file_path9 = '37_83.csv'
csv_file_path10 = '47_73.csv'
csv_file_path11 = '61_71.csv'
csv_file_path12 = '79_89.csv'


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
with open(csv_file_path10, 'r') as file:
    csv_reader = csv.reader(file)
#    data_list = []
    for line in csv_reader:
        data_list.append([int(x) for x in line])
with open(csv_file_path11, 'r') as file:
    csv_reader = csv.reader(file)
#    data_list = []
    for line in csv_reader:
        data_list.append([int(x) for x in line])
with open(csv_file_path12, 'r') as file:
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

newlist = [(i*90)+11 for i in flat_list]
plt.plot(newlist, "x")
plt.show()
print(Counter(newlist))




