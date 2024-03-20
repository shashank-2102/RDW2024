import unittest
from Speed_Limit import Speed_Limit
from RT import RT

class SL_Logic_Test(unittest.TestCase):
    
    def test_SL_Logic_15(self):
        # Instantiate Traffic_Light
        tSpeed = 10
        Distance = 10
        data = {
            '10':[],
            '15':[1, 0.2, 0.4, 0.7],
            '20':[]
        }
        speed_limit_instance = Speed_Limit()

        # Assert the expected behavior
        self.assertEqual(speed_limit_instance.speed_sign(data, tSpeed, Distance) , [15, 0.7, True]) #set correct value


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

        
        # Assert the expected behavior
        self.assertEqual(speed_limit_instance.speed_sign(data, tSpeed, Distance) , [20, 0, True]) #set correct value

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
        self.assertEqual(speed_limit_instance.speed_sign(data, tSpeed, Distance) , [10, 0, False]) #set correct value

if __name__ == '__main__':
    unittest.main()
