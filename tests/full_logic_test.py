import unittest
from central_Logic import priorityDecider, finalFunction
from Lane_Keeping_Maneouvre import Lane_Keeping_Maneouvre
from Pedestrian_Manoeuvre import Pedestrian_Maneouvre
from Speed_Limit import Speed_Limit
from Area_Calculator import Calculate_area
from Traffic_Light import Traffic_Light
from RT import RT


def create_speed_sign():
    data = {
        '10':[],
        '15':[1, 0.2, 0.4, 0.7],
        '20':[]
    }
    tSpeed = 10
    Distance = 10

    return Speed_Limit()

def create_traffic_light():
    color1 = "red"
    coordinates1 = [0.6, 0.3, 0.7, 0.5]

    return Traffic_Light()

def create_ped():
    coordinates1 = [0.4, 0.5, 0.7, 0.6]
    result1 = True
    result2 = True
    result3 = True

    return Pedestrian_Maneouvre()

speed_limit_instance = create_speed_sign()
Pedestrian_instance = create_ped()
traffic_light_instance = create_traffic_light()
lane_keeping = Lane_Keeping_Maneouvre()


obstacle1 = []
obstacle2 = [speed_limit_instance, traffic_light_instance]
obstacle3 = [speed_limit_instance, Pedestrian_instance, traffic_light_instance]

class full_logic_test(unittest.TestCase):
    def test_Func1_empty(self):
        # Empty object list
        objectList = obstacle1 
        self.assertEqual(finalFunction(objectList, False, lane_keeping), [0, float('inf'), 0])

    def test_Func1_one(self):
        # Object list with one object
        objectList = obstacle2
        self.assertEqual(finalFunction(objectList, False, lane_keeping), [30, 20, 0])

    def test_Func1_multi(self):
        # Object list with multiple objects
        objectList = obstacle3
        self.assertEqual(finalFunction(objectList, False, lane_keeping), [30, 20, 0])

    


if __name__ == '__main__':
    unittest.main()