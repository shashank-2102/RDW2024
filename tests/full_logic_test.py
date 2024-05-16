import unittest
from central_Logic import priorityDecider, finalFunction, updateObjectList, clearObjectList, getObjectList
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

    speed_limit_instance = Speed_Limit()
    speed_limit_instance.speed_sign(data, tSpeed, Distance)

    return speed_limit_instance

def create_traffic_light():
    color1 = "red"
    coordinates1 = [0.1, 0.1, 0.1, 0.1]

    traffic_light_instance = Traffic_Light()
    traffic_light_instance.TL_Logic(color1, coordinates1)

    return traffic_light_instance

def create_ped():
    coordinates1 = [0.8, 0.8, 0.9, 0.9]
    result1 = True
    result2 = True
    result3 = True

    Pedestrian_instance = Pedestrian_Maneouvre()
    Pedestrian_instance.pedestrian_logic(result1, result2, result3)

    return Pedestrian_instance


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
        self.assertEqual(finalFunction(obstacle1, False, lane_keeping), [0, float('inf'), 0]) #speed, distance, angle

    def test_Func1_one(self):
        # Object list with one object
        #self.assertEqual(finalFunction(objectList, False, lane_keeping), [15, 20, 0])
        self.assertEqual(finalFunction(obstacle2, False, lane_keeping)[0], 15)
        self.assertEqual(finalFunction(obstacle2, False, lane_keeping)[2], 0)

    def test_Func1_multi(self):
        # Object list with multiple objects
        #self.assertEqual(finalFunction(objectList, False, lane_keeping), [15, 20, 0])
        self.assertEqual(finalFunction(obstacle3, False, lane_keeping)[0], 15)
        self.assertEqual(finalFunction(obstacle3, False, lane_keeping)[2], 0)



class object_list_test(unittest.TestCase):
    def test_OL_empty(self):
        clearObjectList()
        self.assertEqual(len(getObjectList()), 0)

    ##create better tests###
        


if __name__ == '__main__':
    unittest.main()