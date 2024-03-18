import unittest
from Logic_Thread.Maneouvres.Speed_Limit import Speed_Limit
#from RDWLogic.RT import RT

class SL_Logic_Test(unittest.TestCase):
    
    def test_SL_Logic_15(self):
        # Instantiate Traffic_Light
        #test
        tSpeed = 10
        Distance = 10
        data = {
            '10':[],
            '15':[1, 0.2, 0.4, 0.7],
            '20':[]
        }
        speed_limit_instance = Speed_Limit()
        Speed_limit_detected, tSpeed, Distance = speed_limit_instance.speed_sign(data, tSpeed, Distance)
        print(Speed_limit_detected, tSpeed, Distance)
        
        # Assert the expected behavior
        self.assertEqual(True, 15, 0)
        #self.assertEqual(distance, expected_distance)

    def test_SL_Logic_20(self):
        # Instantiate Traffic_Light
        #test
        tSpeed = 10
        Distance = 10
        data = {
            '10':[],
            '15':[],
            '20':[1, 0.2, 0.4, 0.7]
        }
        speed_limit_instance = Speed_Limit()
        Speed_limit_detected, tSpeed, Distance = speed_limit_instance.speed_sign(data, tSpeed, Distance)
        print(Speed_limit_detected, tSpeed, Distance)
        
        # Assert the expected behavior
        self.assertEqual(True, 20, 0)
        #self.assertEqual(distance, expected_distance)

    def test_SL_Logic_None(self):
        # Instantiate Traffic_Light
        #test
        tSpeed = 10
        Distance = 10
        data = {
            '10':[],
            '15':[],
            '20':[]
        }
        speed_limit_instance = Speed_Limit()
        Speed_limit_detected, tSpeed, Distance = speed_limit_instance.speed_sign(data, tSpeed, Distance)
        print(Speed_limit_detected, tSpeed, Distance)
        
        # Assert the expected behavior
        self.assertEqual(False, 10, Distance)
        #self.assertEqual(distance, expected_distance)

if __name__ == '__main__':
    unittest.main()
