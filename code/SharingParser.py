from MMS import MMS
import numpy as np
import pandas as pd
import os
import sys

#input: the file directory with your csv files

input = f"./{sys.argv[1]}"
notMMS = list()

#Function to create a shared matrix
def share(costMatrix):
    sharedMatrix = list()
    for i in range(0, costMatrix.shape[0]):
        currentRow = list()
        for j in range (0, costMatrix.shape[1]):
            currentRow.append(costMatrix[i][j]/2)
            currentRow.append(costMatrix[i][j]/2)
        sharedMatrix.append(currentRow)
    return np.array(sharedMatrix)

#Function to check if an allocation exists were MMS is satisfied given a CSV file directory
def checkMMS(file):
    #open the file
    df = pd.read_csv(file)
    print(f"current file: {file}")

    costMatrix = df.to_numpy(dtype = np.float64)

    #Run the tests
    test = MMS(costMatrix)
    hasMMS = test.existMMS()
    sat = test.satisfiesMMS
    MMSArr = test.MMSArray

    #If it doesn't exist, add it to the failure array
    if not hasMMS:
        newCostMatrix = share(costMatrix)
        costMatrix = newCostMatrix
        shareTest = MMS(newCostMatrix)
        shareTest.MMSArray = MMSArr

        hasMMS = shareTest.existMMS()
        sat = shareTest.satisfiesMMS
        if not hasMMS:
            print("failure point")
            pair = [file, costMatrix]
            notMMS.append(pair)

    print(f"MMS array: {test.MMSArray}, Allocation: {hasMMS}")

    if sat:
        print(f"Cost matrix: \n{costMatrix}")
        print(f"MMS array: {MMSArr}")
        print(f"recieved values: {calculateUtility(sat, costMatrix)}")

def calculateUtility(sat, costMatrix):
    #Create a list of each agent and their total util
    results = list()

    #Go through all the allocations from the satisfaction array
    for al in sat:
        toAdd = list()
        toAdd.append(int(al[0]))
        sum = 0
        #Sum up the utlity of each item in allocation
        for item in al[1]:
            sum += costMatrix[al[0]][item]
        toAdd.append(float(sum))
        results.append(toAdd)
    
    return results
#Checks to see if the user input is valid
if(not os.path.isdir(input) and not os.path.isfile(input)):
    print("ERROR: Please input a valid file directory, or csvfile")
    sys.exit(1)

#Case where its a single file
if(os.path.isfile(input)):
    checkMMS(input)

#Case where it is a directory
else:
    for file in os.listdir(input):
        checkMMS(f"{input}/{file}")

#Print out the results
print("\nProblems without MMS:")
if notMMS:
    for entry in notMMS:
        print(f"filename: {entry[0]}, cost matrix: {entry[1]}")

else:
    print("none :)")

#TODO
#Make it so this code moves through an entire folder full of CSV files
#Make a script which makes randomly generated csv files according to the number of items and agents
#Make it so sharing is accounted for.
#Go to sleep, its currently 3 AM :)
