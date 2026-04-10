import unittest
from fit2004.ass02.assignment2 import crowdedCampus

class TestQ1BruceLi(unittest.TestCase):
    def validate_allocation(self, n, m, timePreferences, proposedClasses, minimumSatisfaction, allocation):
        self.assertIsInstance(allocation, list)
        self.assertEqual(len(allocation), n)
        counts = [0] * m
        satisfied = 0
        for i in range(n):
            class_id = allocation[i]
            self.assertTrue(0 <= class_id < m)
            counts[class_id] += 1
            time_slot = proposedClasses[class_id][0]
            if time_slot in timePreferences[i][:5]:
                satisfied += 1
        for j in range(m):
            min_cap, max_cap = proposedClasses[j][1], proposedClasses[j][2]
            self.assertGreaterEqual(counts[j], min_cap)
            self.assertLessEqual(counts[j], max_cap)
        self.assertGreaterEqual(satisfied, minimumSatisfaction)


    def test1(self):
        n, m = 1, 1
        timePreferences = [list(range(20))]
        proposedClasses = [[0, 1, 1]]
        minimumSatisfaction = 1
        allocation = crowdedCampus(n, m, timePreferences, proposedClasses, minimumSatisfaction)
        self.validate_allocation(n, m, timePreferences, proposedClasses, minimumSatisfaction, allocation)

    def test2(self):
        n, m = 2, 1
        timePreferences = [list(range(20)), list(range(20))]
        proposedClasses = [[0, 2, 2]]
        minimumSatisfaction = 2
        allocation = crowdedCampus(n, m, timePreferences, proposedClasses, minimumSatisfaction)
        self.validate_allocation(n, m, timePreferences, proposedClasses, minimumSatisfaction, allocation)

    def test3(self):
        n, m = 2, 2
        timePreferences = [[1, 0] + list(range(2, 20)), list(range(20))]
        proposedClasses = [[1, 1, 1], [0, 1, 1]]
        minimumSatisfaction = 2
        allocation = crowdedCampus(n, m, timePreferences, proposedClasses, minimumSatisfaction)
        self.validate_allocation(n, m, timePreferences, proposedClasses, minimumSatisfaction, allocation)

    def test4(self):
        n, m = 3, 2
        timePreferences = [[0, 1] + list(range(2, 20)), [1, 0] + list(range(2, 20)), [0, 1] + list(range(2, 20))]
        proposedClasses = [[0, 2, 2], [1, 1, 2]]
        minimumSatisfaction = 3
        allocation = crowdedCampus(n, m, timePreferences, proposedClasses, minimumSatisfaction)
        self.validate_allocation(n, m, timePreferences, proposedClasses, minimumSatisfaction, allocation)

    def test5(self):
        n, m = 4, 2
        timePreferences = [[0, 1] + list(range(2, 20)) for _ in range(2)] + [[1, 0] + list(range(2, 20)) for _ in range(2)]
        proposedClasses = [[0, 2, 2], [1, 2, 2]]
        minimumSatisfaction = 4
        allocation = crowdedCampus(n, m, timePreferences, proposedClasses, minimumSatisfaction)
        self.validate_allocation(n, m, timePreferences, proposedClasses, minimumSatisfaction, allocation)

    def test6(self):
        n, m = 3, 2
        timePreferences = [list(range(20)) for _ in range(3)]
        proposedClasses = [[0, 1, 2], [0, 1, 2]]
        minimumSatisfaction = 3
        allocation = crowdedCampus(n, m, timePreferences, proposedClasses, minimumSatisfaction)
        self.validate_allocation(n, m, timePreferences, proposedClasses, minimumSatisfaction, allocation)

    def test7(self):
        n, m = 4, 2
        timePreferences = [list(range(20)) for _ in range(4)]
        proposedClasses = [[0, 2, 2], [0, 2, 2]]
        minimumSatisfaction = 4
        allocation = crowdedCampus(n, m, timePreferences, proposedClasses, minimumSatisfaction)
        self.validate_allocation(n, m, timePreferences, proposedClasses, minimumSatisfaction, allocation)

    def test8(self):
        n, m = 3, 2
        timePreferences = [
            [0,1,2,3,4] + [t for t in range(20) if t not in [0,1,2,3,4]],
            [0,1,2,3,4] + [t for t in range(20) if t not in [0,1,2,3,4]],
            [1,0,2,3,4] + [t for t in range(20) if t not in [1,0,2,3,4]]
        ]
        proposedClasses = [[0, 2, 2], [1, 1, 2]]
        minimumSatisfaction = 2
        allocation = crowdedCampus(n, m, timePreferences, proposedClasses, minimumSatisfaction)
        self.validate_allocation(n, m, timePreferences, proposedClasses, minimumSatisfaction, allocation)
    


    def test9(self):
        n, m = 1, 1
        timePreferences = [[0] + list(range(1, 20))]
        proposedClasses = [[0, 1, 1]]
        minimumSatisfaction = 1
        allocation = crowdedCampus(n, m, timePreferences, proposedClasses, minimumSatisfaction)
        self.validate_allocation(n, m, timePreferences, proposedClasses, minimumSatisfaction, allocation)

    def test10(self):
        n, m = 4, 2
        timePreferences = [[0] + list(range(1, 20))] * 4
        proposedClasses = [[0, 2, 2], [0, 2, 2]]
        minimumSatisfaction = 4
        allocation = crowdedCampus(n, m, timePreferences, proposedClasses, minimumSatisfaction)
        self.validate_allocation(n, m, timePreferences, proposedClasses, minimumSatisfaction, allocation)

    def test11(self):
        n, m = 3, 2
        timePreferences = [list(range(20)) for _ in range(n)]
        proposedClasses = [[0, 2, 3], [1, 2, 3]]
        minimumSatisfaction = 0
        allocation = crowdedCampus(n, m, timePreferences, proposedClasses, minimumSatisfaction)
        self.assertIsNone(allocation)

    def test12(self):
        n, m = 5, 2
        timePreferences = [
            [0] + list(range(1, 20)),
            [0] + list(range(1, 20)),
            [0] + list(range(1, 20)),
            [1] + list(range(2, 20)) + [0],
            [1] + list(range(2, 20)) + [0]
        ]
        proposedClasses = [[0, 1, 3], [1, 1, 3]]
        minimumSatisfaction = 3
        allocation = crowdedCampus(n, m, timePreferences, proposedClasses, minimumSatisfaction)
        self.validate_allocation(n, m, timePreferences, proposedClasses, minimumSatisfaction, allocation)


    def test13(self):
        n = 5
        m = 1
        timePreferences = [list(range(20)) for _ in range(n)]
        proposedClasses = [[0, 5, 5]]
        minimumSatisfaction = 5
        allocation = crowdedCampus(n, m, timePreferences, proposedClasses, minimumSatisfaction)
        self.validate_allocation(n, m, timePreferences, proposedClasses, minimumSatisfaction, allocation)

    def test14(self):
        n = 6
        m = 3
        timePreferences = [[j] + list(range(20)) for j in [0, 0, 1, 1, 2, 2]]
        proposedClasses = [[0, 2, 2], [1, 2, 2], [2, 2, 2]]
        minimumSatisfaction = 6
        allocation = crowdedCampus(n, m, timePreferences, proposedClasses, minimumSatisfaction)
        self.validate_allocation(n, m, timePreferences, proposedClasses, minimumSatisfaction, allocation)

    def test15(self):
        n = 4
        m = 2
        timePreferences = [[19,18,17,16,15] + list(range(15)) for _ in range(n)]
        proposedClasses = [[0, 2, 3], [1, 1, 2]]
        minimumSatisfaction = 4
        allocation = crowdedCampus(n, m, timePreferences, proposedClasses, minimumSatisfaction)
        self.assertIsNone(allocation)

    def test16(self):
        n = 6
        m = 2
        timePreferences = [[5] + list(range(20)) for _ in range(n)]
        proposedClasses = [[5, 3, 3], [5, 3, 3]]
        minimumSatisfaction = 6
        allocation = crowdedCampus(n, m, timePreferences, proposedClasses, minimumSatisfaction)
        self.validate_allocation(n, m, timePreferences, proposedClasses, minimumSatisfaction, allocation)

    def test17(self):
        n = 4
        m = 2
        timePreferences = [[0] + list(range(1, 20)),
                            [1] + list(range(2, 20)) + [0],
                            [1] + list(range(2, 20)) + [0],
                            [2] + list(range(3, 20)) + [0]+[1]]
        proposedClasses = [[0, 1, 2], [1, 1, 2]]
        minimumSatisfaction = 2
        allocation = crowdedCampus(n, m, timePreferences, proposedClasses, minimumSatisfaction)
        self.validate_allocation(n, m, timePreferences, proposedClasses, minimumSatisfaction, allocation)

    def test18(self):
        n = 10
        m = 2
        timePreferences = [[5] + [t for t in range(20) if t != 5] for _ in range(n)]
        proposedClasses = [[5, 1, 6], [5, 1, 6]]
        minimumSatisfaction = 10
        allocation = crowdedCampus(n, m, timePreferences, proposedClasses, minimumSatisfaction)
        self.validate_allocation(n, m, timePreferences, proposedClasses, minimumSatisfaction, allocation)

    def test19(self):
        n = 5
        m = 2
        timePreferences = [
            [0] + list(range(1, 20)),
            [0] + list(range(1, 20)),
            [0] + list(range(1, 20)),
            [0] + list(range(1, 20)),
            [0] + list(range(1, 20))
        ]
        proposedClasses = [[19, 2, 3], [19, 2, 3]]
        minimumSatisfaction = 1
        allocation = crowdedCampus(n, m, timePreferences, proposedClasses, minimumSatisfaction)
        self.assertIsNone(allocation)
        
    def test20(self):
        n = 10
        m = 2
        timePreferences = [list(range(20)) for _ in range(n)]
        proposedClasses = [[0, 1, 4], [1, 1, 4]]
        minimumSatisfaction = 0
        allocation = crowdedCampus(n, m, timePreferences, proposedClasses, minimumSatisfaction)
        self.assertIsNone(allocation)

    def test21(self):
        n = 10
        m = 2
        timePreferences = [list(range(20)) for _ in range(n)]
        proposedClasses = [[0, 5, 5], [1, 5, 5]]
        minimumSatisfaction = 0
        allocation = crowdedCampus(n, m, timePreferences, proposedClasses, minimumSatisfaction)
        self.validate_allocation(n, m, timePreferences, proposedClasses, minimumSatisfaction, allocation)

    def test22(self):
            n = 4
            m = 2
            timePreferences = [[0] + list(range(1, 20)),
                                [0] + list(range(1, 20)),
                                [0] + list(range(1, 20)),
                                [0] + list(range(1, 20))]
            proposedClasses = [[0, 1, 20], [5, 3, 20]]
            minimumSatisfaction = 1
        
            allocation = crowdedCampus(n, m, timePreferences, proposedClasses, minimumSatisfaction)
            self.validate_allocation(n, m, timePreferences, proposedClasses, minimumSatisfaction, allocation)
            
    def test23(self):
            n = 7
            m = 3
            timePreferences = [[0] + list(range(1, 20)),
                                [0] + list(range(1, 20)),
                                [0] + list(range(1, 20)),
                                [0] + list(range(1, 20)),
                                [0] + list(range(1, 20)),
                                [0] + list(range(1, 20)),
                                [0] + list(range(1, 20))]

            proposedClasses = [[0, 1, 20], [0, 3, 5] ,[5, 3, 20]]
            minimumSatisfaction = 2
            allocation = crowdedCampus(n, m, timePreferences, proposedClasses, minimumSatisfaction)
            self.validate_allocation(n, m, timePreferences, proposedClasses, minimumSatisfaction, allocation)


    def test24(self):
        n = 8
        m = 2
        minimumSatisfaction = 6          
        timePreferences = [
            [0, 1] + list(range(2, 20))  for _ in range(n)]

        proposedClasses = [[0, 4, 8],   [1, 4, 8],   ]
        allocation = crowdedCampus(n, m, timePreferences, proposedClasses, minimumSatisfaction)
        self.validate_allocation(n, m, timePreferences, proposedClasses, minimumSatisfaction, allocation)

    def test25(self):
        n = 2
        m = 2
        timePreferences = [
            [0, 1, 2, 3, 4] + list(range(5, 20)),
            [1, 2, 3, 4, 0] + list(range(5, 20)),
        ]
        proposedClasses = [
            [0, 2, 3],
            [1, 1, 2],
        ]
        minimumSatisfaction = 2
        allocation = crowdedCampus(n,m,timePreferences,proposedClasses,minimumSatisfaction)
        self.assertIsNone(allocation)

    def test26(self):
        n = 3
        m = 2
        timePreferences = [
            [0, 1, 2, 3, 4] + list(range(5, 20)),
            [1, 2, 3, 4, 0] + list(range(5, 20)),
            [0, 1, 2, 3, 4] + list(range(5, 20)),
        ]
        proposedClasses = [
            [0, 2, 3],
            [1, 1, 2],
        ]
        minimumSatisfaction = 3
        allocation = crowdedCampus(n,m,timePreferences,proposedClasses,minimumSatisfaction)
        self.validate_allocation(n,m,timePreferences,proposedClasses,minimumSatisfaction, allocation)

    def test27(self):
        n = 4
        m = 2
        timePreferences = [
            [0, 1, 2, 3, 4] + list(range(5, 20)),
            [0, 1, 2, 3, 4] + list(range(5, 20)),
            [1, 0, 2, 3, 4] + list(range(5, 20)),
            [1, 0, 2, 3, 4] + list(range(5, 20)),
        ]
        proposedClasses = [
            [0, 2, 2],
            [1, 2, 2],
        ]
        minimumSatisfaction = 4
        allocation = crowdedCampus(n,m,timePreferences,proposedClasses,minimumSatisfaction)
        self.validate_allocation(n,m,timePreferences,proposedClasses,minimumSatisfaction, allocation)

    def test28(self):
        n = 50
        m = 5
        timePreferences = [list(range(20)) for _ in range(n)]
        proposedClasses = [[i, 10, 15] for i in range(5)]
        minimumSatisfaction = 40
        allocation = crowdedCampus(n,m,timePreferences,proposedClasses,minimumSatisfaction)
        self.validate_allocation(n,m,timePreferences,proposedClasses,minimumSatisfaction, allocation)

    def test29(self):
        n = 4
        m = 2
        timePreferences = [
            [10, 11, 12, 13, 14] + [i for i in range(20) if i not in [10,11,12,13,14]],
            [10, 11, 12, 13, 14] + [i for i in range(20) if i not in [10,11,12,13,14]],
            [10, 11, 12, 13, 14] + [i for i in range(20) if i not in [10,11,12,13,14]],
            [10, 11, 12, 13, 14] + [i for i in range(20) if i not in [10,11,12,13,14]],
        ]
        proposedClasses = [
            [0, 2, 4],
            [1, 2, 4],
        ]
        minimumSatisfaction = 1
        allocation = crowdedCampus(n,m,timePreferences,proposedClasses,minimumSatisfaction)
        self.assertIsNone(allocation)

    def test30(self):
        n = 3
        m = 2
        timePreferences = [
            [0, 1, 2, 3, 4] + list(range(5, 20)),
            [1, 2, 3, 4, 0] + list(range(5, 20)),
            [0, 1, 2, 3, 4] + list(range(5, 20)),
        ]
        proposedClasses = [
            [0, 2, 3],
            [1, 2, 3],
        ]
        minimumSatisfaction = 3
        allocation = crowdedCampus(n,m,timePreferences,proposedClasses,minimumSatisfaction)
        self.assertIsNone(allocation)

    def test31(self):
        n = 4
        m = 2
        timePreferences = [
            [5, 6, 7, 8, 9] + [i for i in range(20) if i not in [5,6,7,8,9]],
            [5, 6, 7, 8, 9] + [i for i in range(20) if i not in [5,6,7,8,9]],
            [5, 6, 7, 8, 9] + [i for i in range(20) if i not in [5,6,7,8,9]],
            [5, 6, 7, 8, 9] + [i for i in range(20) if i not in [5,6,7,8,9]],
        ]
        proposedClasses = [
            [0, 2, 3],
            [1, 2, 3],
        ]
        minimumSatisfaction = 1
        allocation = crowdedCampus(n,m,timePreferences,proposedClasses,minimumSatisfaction)
        self.assertIsNone(allocation)

    def test32(self):
        n = 4
        m = 2
        timePreferences = [
            [0, 1, 2, 3, 4] + list(range(5, 20)),
            [0, 1, 2, 3, 4] + list(range(5, 20)),
            [0, 1, 2, 3, 4] + list(range(5, 20)),
            [0, 1, 2, 3, 4] + list(range(5, 20)),
        ]
        proposedClasses = [
            [0, 2, 4],
            [1, 1, 3],
        ]
        minimumSatisfaction = 4
        allocation = crowdedCampus(n,m,timePreferences,proposedClasses,minimumSatisfaction)
        self.validate_allocation(n,m,timePreferences,proposedClasses,minimumSatisfaction, allocation)

    def test33(self):
        n = 4
        m = 2
        timePreferences = [
            [5, 6, 7, 8, 9] + [i for i in range(20) if i not in [5,6,7,8,9]],
            [5, 6, 7, 8, 9] + [i for i in range(20) if i not in [5,6,7,8,9]],
            [5, 6, 7, 8, 9] + [i for i in range(20) if i not in [5,6,7,8,9]],
            [5, 6, 7, 8, 9] + [i for i in range(20) if i not in [5,6,7,8,9]],
        ]
        proposedClasses = [
            [0, 2, 4],
            [1, 2, 4],
        ]
        minimumSatisfaction= 1
        allocation = crowdedCampus(n,m,timePreferences,proposedClasses,minimumSatisfaction)
        self.assertIsNone(allocation)
    
    def test34(self):
        n = 3
        m = 2
        timePreferences = [
            [0, 1, 2, 3, 4] + list(range(5, 20)),     
            [0, 1, 2, 3, 4]+ list(range(5, 20)),     
            [5, 6, 7, 8, 9] + [0,1,2,3,4] + list(range(10,20))   
        ]
        proposedClasses = [
            [0, 1, 2], 
            [1, 1, 2], 
        ]
        minimumSatisfaction = 3
        allocation = crowdedCampus(n,m,timePreferences,proposedClasses,minimumSatisfaction)
        self.assertIsNone(allocation)    

    def test35(self):
        n, m = 3, 2
        proposedClasses = [
            [0, 2, 3],  
            [1, 1, 3],  
        ]
        timePreferences = [
            [0, 1, 2, 3, 4] + list(range(5, 20)),  
            [1, 2, 3, 4, 5] + list(range(6, 20)) + [0],  
            [5, 6, 7, 8, 9] + list(range(0, 5)) + list(range(10, 20)),  
        ]
        minimumSatisfaction = 1
        allocation = crowdedCampus(n, m, timePreferences, proposedClasses, minimumSatisfaction)
        self.validate_allocation(n,m,timePreferences,proposedClasses,minimumSatisfaction,allocation)

    def test36(self):
        n = 5  
        m = 2  
        timePreferences = [
            [0, 1, 2, 3, 4],
            [0, 1, 2, 3, 4],
            [0, 1, 2, 3, 4],
            [0, 1, 2, 3, 4],
            [0, 1, 2, 3, 4],
        ]
        proposedClasses = [
            [0, 1, 5],
            [1, 2, 5],
        ]
        minimumSatisfaction = 5  
        allocation = crowdedCampus(n,m,timePreferences,proposedClasses,minimumSatisfaction)
        self.validate_allocation(n,m,timePreferences,proposedClasses,minimumSatisfaction,allocation)

    def test37(self):
        n = 4  
        m = 2  

        
        
        
        timePreferences = [
            [0]+ list(range(2, 20)),  
            [0]+ list(range(2, 20)),  
            [1]+ list(range(2, 20)),  
            [1]+ list(range(2, 20)),  
        ]
        
        
        proposedClasses = [
            (0, 1, 3),  
            (1, 1, 3),  
        ]

        
        minimumSatisfaction = 4
        allocation = crowdedCampus(n,m,timePreferences,proposedClasses,minimumSatisfaction)
        self.validate_allocation(n,m,timePreferences,proposedClasses,minimumSatisfaction,allocation)
    
    def test38(self):
        n = 6
        m = 3 
        timePreferences = [
            [0, 1] + list(range(2, 20)),   
            [0, 1] + list(range(2, 20)),   
            [1, 0] + list(range(2, 20)),   
            [1, 0] + list(range(2, 20)),   
            [0, 1] + list(range(2, 20)),   
            [2, 0] + list(range(2, 20)) + [1],  
        ]
        proposedClasses = [
            (0, 2, 6),   
            (1, 2, 4),   
            (2, 1, 5),   
        ]
        minimumSatisfaction = 6  
        allocation = crowdedCampus(n, m, timePreferences, proposedClasses, minimumSatisfaction)
        self.validate_allocation(n,m,timePreferences,proposedClasses,minimumSatisfaction,allocation)
    
    def test39(self):
        n = 3
        m = 2
        timePreferences = [
            [0] + list(range(2, 20)),  
            [0] + list(range(2, 20)), 
            [0] + list(range(2, 20)),  
        ]
        proposedClasses = [
            (0, 0, 3),  
            (1, 2, 3),  
        ]
        minimumSatisfaction = 3  
        allocation = crowdedCampus(n, m, timePreferences, proposedClasses, minimumSatisfaction)
        self.assertIsNone(allocation)
    
    def test40(self):
        n = 2
        m = 2
        timePreferences = [
            [0] + list(range(2, 20)),
            [1] + list(range(2, 20)),  
        ]
        proposedClasses = [
            (0, 2, 2),  
            (1, 2, 2),  
        ]
        minimumSatisfaction = 2  
        allocation = crowdedCampus(n, m, timePreferences, proposedClasses, minimumSatisfaction)
        self.assertIsNone(allocation)
    
    def test41(self):
        n = 3
        m = 2
        timePreferences = [
            [0] + list(range(2, 20)),  
            [0] + list(range(2, 20)),  
            [0] + list(range(2, 20)),  
        ]
        proposedClasses = [
            (0, 0, 3),  
            (1, 2, 2), 
        ]
        minimumSatisfaction = 3
        allocation = crowdedCampus(n, m, timePreferences, proposedClasses, minimumSatisfaction)
        self.assertIsNone(allocation)
    
    def test42(self):
        n = 4
        m = 2
        timePreferences = [
            [0] + list(range(1, 20)),  
            [0] + list(range(1, 20)),  
            [0] + list(range(1, 20)),  
            [0] + list(range(1, 20)),  
        ]
        proposedClasses = [
            (0, 2, 4),
            (1, 2, 2),  
        ]
        minimumSatisfaction = 2  
        allocation = crowdedCampus(n, m, timePreferences, proposedClasses, minimumSatisfaction)
        self.validate_allocation(n,m,timePreferences,proposedClasses,minimumSatisfaction,allocation)
    
    def test43(self):
        n = 3
        m = 2
        timePreferences = [
            [0, 1] + list(range(2, 20)), 
            [1, 0] + list(range(2, 20)),  
            [1, 0] + list(range(2, 20)),  
        ]
        proposedClasses = [
            (0, 1, 2),  
            (1, 2, 2), 
        ]
        minimumSatisfaction = 3
        allocation = crowdedCampus(n, m, timePreferences, proposedClasses, minimumSatisfaction)
        self.validate_allocation(n,m,timePreferences,proposedClasses,minimumSatisfaction,allocation)
    
    def test44(self):
        n = 6
        m = 2
        timePreferences = [list(range(0, 20))] * 6
        proposedClasses = [[0, 5, 10], [5, 1, 10]]
        minimumSatisfaction = 6
        allocation = crowdedCampus(n, m, timePreferences, proposedClasses, minimumSatisfaction)
        self.assertIsNone(allocation)


if __name__ == "__main__":
    unittest.main(verbosity=2)
