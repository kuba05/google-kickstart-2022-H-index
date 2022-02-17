from math import log2, ceil 

from time import time_ns, sleep
import sys
import unittest
import random

timeHalving = timeAdding = timeCalculatingHIndex = 0

class Solve():
    def __init__(self, N):
        self.array = [0] * N
        self.size = 0
        self.lastHIndex = 0
    
    @staticmethod    
    def solve(N, Cx):
        solver = Solve(N)
        output = [0] * N
        
        for i, study in enumerate(Cx):
            output[i] = solver._add_and_process(study)
            # if any(array[j-1] > array[j] for j in range(1, i + 1)):
            #    sys.exit(1)
            
        return output
    
    
    def _add_and_process(self, item):
        """
        index is the first index that is not used yet (all non-used elements shall be 0)
        """
        
        global timeHalving, timeAdding, timeCalculatingHIndex
        time_0 = time_ns()
        ## binary search with normalization
        i = 0
        if self.size >= 2:
            i = 2**(ceil(log2(self.size))-1) - 1
            step = (i+1) // 2
            if self.array[i] > item:
                i = self.size - 1 - i
            else:
                i -= step
                step //= 2
            while step >= 1:
                if self.array[i] == item:
                    break
                if self.array[i] > item:
                    i += step
                else:
                    i -= step
                step //= 2
        
        time_1 = time_ns()
        
        if self.size > 0 and self.array[i] > item:
            i += 1
            # insert            
        for j in range(self.size, i, -1):
            self.array[j] = self.array[j - 1]
        self.array[i] = item
        self.size += 1
        
        time_2 = time_ns()
        # compute HIndex
        
        #if i is too big, it couldn't have influenced HIndex in any way
        if i <= self.lastHIndex:
            #the change of HIndex can be at most by 1, so it is sufficient to check the first element after the already checked sequence 
            if self.array[self.lastHIndex] > self.lastHIndex:
                self.lastHIndex += 1
        
        
        time_3 = time_ns()
        
        timeHalving += time_1 - time_0
        
        timeAdding += time_2 - time_1
        
        timeCalculatingHIndex += time_3 - time_2
        return self.lastHIndex
        
    
def main():    
    for i in range(int(input())):
        N = int(input())
        Cx = [int(x) for x in input().split()]
        assert(N == len(Cx))
    
        print(f"Case #{i+1}:", *Solve.solve(N, Cx))
    
    


class TestMain(unittest.TestCase):
    
    def test_allSets(self):
        datasets = [
            [
                [5, 2, 1, 3],
                [1, 2, 2, 2]
            ],
            [
                [random.randint(1,10**5) for i in range(10**4)],
                []
            ]
        ]
        for data, output in datasets:
            self.assertEqual(self.dataSetTest(data), output)
            
            
    def dataSetTest(self, data):
        return Solve.solve(len(data), data)
        
    @classmethod
    def tearDownClass(cls):
        print(f"timeAdding: {timeAdding}", file=sys.stderr)
        print(f"timeHalving: {timeHalving}", file=sys.stderr)
        print(f"timeCalculatingHIndex: {timeCalculatingHIndex}", file=sys.stderr)
        

if __name__ == "__main__":
    main()
  
  
"""
data = [5,2,1,3]
output = [1, 2, 2, 2]
"""