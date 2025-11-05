import sys
from itertools import combinations
from itertools import permutations
import numpy as np

class MMS:
    Allocations = set()

    agents = None
    goods = set()

    agentCount = 0

    #costsArray => (agentNum, goodNum)
    costsArray = None

    MMSArray = None

    satisfiesMMS = None

    def __init__(self, input):
        self.costsArray = input.astype(np.float128)
        self.agents = np.arange(0, self.costsArray.shape[0], dtype = np.uint64)
        self.goods = set(np.arange(0, self.costsArray.shape[1], dtype = np.uint64))
        
        
        self.agentCount = self.agents.shape[0]
        # print(self.agentCount)
        self.MMSArray = np.full((self.agentCount), -1)
        # print(self.MMSArray)

        self.PopulateAllAllocations(self.goods, self.agentCount, self.FindMMSArray) #populate the MMS array
        # self.Allocations = self.PopulateAllAllocations(self.goods, self.agentCount)
        # self.MMSArray = self.FindMMSArray()



    
    #AI created this function to find all integer partitions
    def FindIntegerPartition(self, n, k, max_val=None):
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
            for rest_of_partition in self.FindIntegerPartition(n - first_part, k - 1, first_part):
                yield (first_part,) + rest_of_partition

    #Finds all possible allocations given a set, and desired sizes of subsets
    def FindAllocations(self, subsetLengths, testSubset, setOfAllocations, subsetPtr, currentSubset, func):
        for combo in combinations(testSubset, subsetLengths[subsetPtr]):
            nextSubset = currentSubset[:]
            nextSubset.append(combo)
            if(subsetPtr == len(subsetLengths) - 1):
                # print(frozenset(nextSubset))
                # setOfAllocations.add(frozenset(nextSubset))
                func(frozenset(nextSubset))
                return
            nonAllocatedItems = testSubset.copy().difference(combo)
            self.FindAllocations(subsetLengths, nonAllocatedItems, setOfAllocations, subsetPtr+1, nextSubset, func)
    
    #Returns a list of all possible allocations for a given allocation problem
    def PopulateAllAllocations(self, inputSet, numberOfAgents, func):
        intgerPartions = list(self.FindIntegerPartition(len(inputSet), numberOfAgents))
        allAllocations = set()
        for partition in intgerPartions:
            subAllocations = set()
            self.FindAllocations(partition, inputSet, subAllocations, 0, list(), func)
            allAllocations = allAllocations | subAllocations
        return allAllocations
    
    #takes a costsArray, and returns the MMS for each agent
    def FindMMSArray(self, al):
        #ID in the array corresponds to MMS value for that given agent
        for i in self.agents:
            currentMMS = self.MMSArray[i]
            current = sys.maxsize
            for sub in al:
                sum = 0
                for item in sub:
                    sum += self.costsArray[i][item]
                current = min([sum, current])
            currentMMS = max([current, currentMMS])
            self.MMSArray[i] = currentMMS   

    #Sees if there exists any allocations where MMS is satisfied
    def existMMSHelper(self, allocation):
        #creates agents array
        agents = np.arange(0, self.costsArray.shape[0], dtype = np.uint8)

        perms = permutations(allocation)
        isMMS = True
        for perm in perms:
            currentAl = list(zip(agents, perm))
            for al in currentAl:
                currentSum = 0
                for i in al[1]:
                    currentSum += self.costsArray[al[0]][i]
                isMMS = currentSum >= self.MMSArray[al[0]]
                if not isMMS:
                    break
            if(isMMS):
                self.satisfiesMMS = currentAl
                return
            else:
                isMMS = True

    
    def existMMS(self):
        self.PopulateAllAllocations(self.goods, self.agentCount, self.existMMSHelper)
        return self.satisfiesMMS

    
    
# test = MMS(np.array([[1,1,1],[1,1,1]]))
# print(test.MMSArray)
# print(test.existMMS())
