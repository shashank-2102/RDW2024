import unittest
from Speed_Limit import Speed_Limit
from RT import RT

class SL_Logic_Test(unittest.TestCase):
    
    def test_SL_Logic_15(self):
        # Instantiate Traffic_Light
        tSpeed = 10
        coords = [10, 5, 2, 4]
        speed_limit_instance = Speed_Limit()

        # Assert the expected behavior
        self.assertEqual(speed_limit_instance.speed_sign(tSpeed, coords) , [15, 0]) #set correct value


    def test_SL_Logic_20(self):
        # Instantiate Traffic_Light
        #test
        tSpeed = 20
        coords = [10, 5, 2, 4]
        speed_limit_instance = Speed_Limit()

        
        # Assert the expected behavior
        self.assertEqual(speed_limit_instance.speed_sign(tSpeed, coords) , [20, 0]) #set correct value

    def test_SL_Logic_None(self):
        # Instantiate Traffic_Light
        #test
        tSpeed = 10
        coords = [1, 3, 4, 5]
        speed_limit_instance = Speed_Limit()
        self.assertEqual(speed_limit_instance.speed_sign(tSpeed, coords) , [10, 0]) #set correct value

if __name__ == '__main__':
    unittest.main()
