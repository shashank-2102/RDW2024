import unittest
from central_logic import Func1

class Test_Obstacle:
    _distance = 0
    _TSpeed = 0
    def __init__(self, distance, TSpeed):
        # Logic
        self.__lane_keeping_maneouvre = None

    def getTSpeed(self):
        return self._TSpeed

    def getDistance(self):
        return self._distance


# Create test obstacle objects
obstacle1 = Test_Obstacle(10, 50)
obstacle2 = Test_Obstacle(20, 30)
obstacle3 = Test_Obstacle(35, 40)



class func1_test(unittest.TestCase):
    def test_Func1_empty(self):
        # Empty object list
        objectList = []
        self.assertEqual(Func1(objectList), [0, 0])

    def test_Func1_one(self):
        # Object list with one object
        objectList = [obstacle1]
        self.assertEqual(Func1(objectList), [50, 10])

    def test_Func1_multi(self):
        # Object list with multiple objects
        objectList = [obstacle1, obstacle2, obstacle3]
        self.assertEqual(Func1(objectList), [50, 10])

    def test_Final_Function(self):
        pass


if __name__ == '__main__':
    unittest.main()