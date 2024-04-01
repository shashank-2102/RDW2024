import unittest
from central_Logic import priorityDecider, finalFunction
from Lane_Keeping_Maneouvre import Lane_Keeping_Maneouvre

class Test_Obstacle:
    _distance = 0
    _TSpeed = 0
    def __init__(self, distance, Speed):
        # Logic
        self.__lane_keeping_maneouvre = None
        self._TSpeed = Speed
        self._distance = distance

    def getTSpeed(self):
        return self._TSpeed

    def getDistance(self):
        return self._distance


# Create test obstacle objects
obstacle1 = Test_Obstacle(10, 50)
obstacle2 = Test_Obstacle(20, 30)
obstacle3 = Test_Obstacle(35, 40)

class priorityDecider_test(unittest.TestCase):
    def test_Func1_empty(self):
        # Empty object list
        objectList = []
        self.assertEqual(priorityDecider(objectList), [0, float('inf')])

    def test_Func1_one(self):
        # Object list with one object
        objectList = [obstacle1]
        self.assertEqual(priorityDecider(objectList), [50, 10])

    def test_Func1_multi(self):
        # Object list with multiple objects
        objectList = [obstacle1, obstacle2, obstacle3]
        self.assertEqual(priorityDecider(objectList), [50, 10])
    
class finalFunction_test(unittest.TestCase):
    def test_finalFunction_single_test(self):
        objectList = [obstacle2]
        lane_keeping = Lane_Keeping_Maneouvre()
        self.assertEqual(finalFunction(objectList, False, lane_keeping), [30, 20, 0])

    def test_finalFunction_multi_test(self):
        objectList = [obstacle1, obstacle2, obstacle3]
        lane_keeping = Lane_Keeping_Maneouvre()
        self.assertEqual(finalFunction(objectList, False, lane_keeping), [50, 10, 0])

    #add test cases


    


if __name__ == '__main__':
    unittest.main()