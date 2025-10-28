import sys
from itertools import combinations
from itertools import permutations
import numpy as np
from scipy.special import stirling2

#print(stirling2(5,2))

Allocations = set()
setOfAllocations = set()

# def findAllocationsExample():
#     test = [2, 2, 1]
#     testSet = {1,2,3,4,5}

#AI created this function to find all integer partitions
def FindIntegerPartition(n, k, max_val=None):
    """
    Generates all integer partitions of 'n' into exactly 'k' parts.

    Args:
        n (int): The integer to partition.
        k (int): The desired number of parts in each partition.
        max_val (int, optional): The maximum value allowed for a part in the partition.
                                 Defaults to 'n' if not provided.

    Yields:
        tuple: A tuple representing an integer partition of 'n' into 'k' parts.
    """
    if max_val is None:
        max_val = n

    if k == 0:
        if n == 0:
            yield ()  # Base case: if n and k are both 0, an empty tuple is a valid partition
        return

    if n <= 0 or k <= 0:
        return

    # Iterate through possible values for the first part
    # The value can range from 1 up to min(n, max_val)
    for first_part in range(1, min(n, max_val) + 1):
        # Recursively find partitions for the remaining sum (n - first_part)
        # with one less part (k - 1) and a new max_val (first_part)
        # to ensure parts are non-increasing (or non-decreasing, depending on desired order)
        for rest_of_partition in FindIntegerPartition(n - first_part, k - 1, first_part):
            yield (first_part,) + rest_of_partition


#Finds all possible allocations given a set, and desired sizes of subsets
def FindAllocations(subsetLengths, testSubset, setOfAllocations, subsetPtr, currentSubset):
     for combo in combinations(testSubset, subsetLengths[subsetPtr]):
          nextSubset = currentSubset[:]
          nextSubset.append(combo)
          if(subsetPtr == len(subsetLengths) - 1):
               setOfAllocations.add(frozenset(nextSubset))
               return
          nonAllocatedItems = testSubset.copy().difference(combo)
          FindAllocations(subsetLengths, nonAllocatedItems, setOfAllocations, subsetPtr+1, nextSubset)

#Returns a list of all possible allocations for a given allocation problem
def PopulateAllAllocations(inputSet, numberOfAgents):
    intgerPartions = list(FindIntegerPartition(len(inputSet), numberOfAgents))
    allAllocations = set()
    for partition in intgerPartions:
        subAllocations = set()
        FindAllocations(partition, inputSet, subAllocations, 0, list())
        allAllocations = allAllocations | subAllocations
    print(len(allAllocations))
    return allAllocations

#takes a costsArray, and returns the MMS for each agent
def FindMMSArray(costsArray):
    #costsArray => (agentNum, goodNum)

    numberOfAgents = costsArray.shape[0]
    agents = np.arange(0, costsArray.shape[0])
    goods = np.arange(0, costsArray.shape[1])

    # print(agents)
    # print(numberOfAgents)

    allocations = PopulateAllAllocations(set(goods), numberOfAgents)
    #ID in the array corresponds to MMS value for that given agent
    MMSArray = np.zeros(numberOfAgents, dtype=np.uint8)

    for i in agents:
        currentMMS = -1
        for al in allocations:
            current = sys.maxsize
            for sub in al:
                sum = 0
                for item in sub:
                    sum += costsArray[i][item]
                current = min([sum, current])
            currentMMS = max([current, currentMMS])
        MMSArray[i] = currentMMS   

    return MMSArray

#Sees if there exists any allocations where MMS is satisfied
def existMMS(MMSArray, costsArray, allocations):
    #creates agents array
    agents = np.arange(0, costsArray.shape[0], dtype = np.uint8)
    for allocation in allocations:
        perms = permutations(allocation)
        isMMS = True
        for perm in perms:
            currentAl = list(zip(agents, perm))
            for al in currentAl:
                currentSum = 0
                for i in al[1]:
                    currentSum += costArray[al[0]][i]
                isMMS = currentSum >= MMSArray[al[0]]
                if not isMMS:
                    break
            if(isMMS):
                # print(currentAl)
                return True
            else:
                isMMS = True

    return False

costArray = np.array([[5,3,1,4,0], 
                      [2,1,2,1,0],
                      [1,2,1,2,0],
                      [0,0,0,1,0]])

allAllocations = PopulateAllAllocations(set(np.arange(0, costArray.shape[1])), 4)

# print(len(allAllocations))
# print(PopulateAllAllocations({0,1}, 2))
agentMMS = FindMMSArray(costArray)
# print(agentMMS)

# print(existMMS(agentMMS, costArray, allAllocations))