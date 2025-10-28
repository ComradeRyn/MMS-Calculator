import sys
import os
import random
import numpy as np
import csv

#Input: n (Number of agents), m (Number of goods), gm (Highest good value), numOfFiles (number of files you wish to create), dest (folder where to place these files) 

agents = int(sys.argv[1])
goods = int(sys.argv[2])
maxValue = int(sys.argv[3])
numOfFiles = int(sys.argv[4])
dest = sys.argv[5]

#Makes a directory if one does not exist
if not os.path.isdir(f"./{dest}"):
    os.mkdir(f"./{dest}")

for i in range(0, numOfFiles + 1):
    #Populate data array with cost matrix
    path = f"./{dest}/test{i}.csv"
    data = np.zeros((agents + 1, goods), dtype=np.uint32)
    data[0] = np.arange(0, goods)

    #Assign random values 
    for n in range(1, agents+1):
        for m in range(0, goods):
            data[n][m] = random.randint(0, maxValue)
    
    #Create the CSV file
    with open(path, 'w', newline= '') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)
    