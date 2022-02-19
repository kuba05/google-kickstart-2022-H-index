from heapq import heappush, heappushpop

from time import time_ns
import sys
import unittest
import random


"""
see the assignment details: https://codingcompetitions.withgoogle.com/kickstart/round/00000000008f4332/0000000000941e56
"""


class Solve():
    def __init__(self, N):
        self.heap = []
        self.lastHIndex = 0
    
    
    @staticmethod    
    def solve(N, Cx):
        """
        static method used for solving tasks
        """
        solver = Solve(N)
        output = [0] * N
        
        for i, study in enumerate(Cx):
            output[i] = solver._add_and_process(study)
        
        return output
    
    
    def _add_and_process(self, item):
        """
            add new paper and recalculate h-index after adding it
        """
        # if a paper has 0 or less citations it can never influence H-index in any way
        if item <= 0:
            return self.lastHIndex
        
        #if there are no previous papers, this one will for sure raise the H-index
        if len(self.heap) == 0:
            self.heap.append(item)
            self.lastHIndex += 1
            return self.lastHIndex
        
        #HIndex can change only either: increase by 1; or not change at all (with each paper added)
        
        # if the new paper has less citations than h-index would be after we raise it, there is no way
        #this paper raises the h-index
        if item <= self.lastHIndex:
            return self.lastHIndex
        
        #if the paper with least citations (which still has more or equal citations than last h-index was)
        #has enough citations for the h-index to raise, we can raise the h-index 
        if self.heap[0] >= self.lastHIndex + 1:
            heappush(self.heap, item)
            self.lastHIndex += 1
            return self.lastHIndex
        
        #else the lowest element in heap shall be removed, since it can no longer contribute to raising h-index
        heappushpop(self.heap, item)
        
        return self.lastHIndex
        
    
def main():
    #there will be K independent tasks
    for i in range(int(input())):
        #for each we need to first parse the input
        N = int(input())
        Cx = [int(x) for x in input().split()]
        
        #make sure the input makes sense
        assert(N == len(Cx))
    
        print(f"Case #{i+1}:", *Solve.solve(N, Cx))
    
    


class TestMain(unittest.TestCase):
    
    def test_allSets(self):
        
        """
        datasets are in format:
        [input, expectedOutput]
        
        where both input and expectedOutput are arrays of numbers of the same length
        """
        datasets = [
            [
                [5, 2, 1, 3],
                [1, 2, 2, 2]
            ],
            [
                [1, 3, 3, 2, 2, 15],
                [1, 1, 2, 2, 2, 3]
            ]
        ]

        for data, output in datasets:
            self.assertEqual(self.dataSetTest(data), output)
            
            
    def dataSetTest(self, data):
        return Solve.solve(len(data), data)
        

if __name__ == "__main__":
    main()