import unittest
from Logic_Thread.Maneouvres.Traffic_Light import Traffic_Light
#from RDWLogic.RT import RT

class TL_Logic_Test(unittest.TestCase):
    
    def test_TL_Logic_red(self):
        # Instantiate Traffic_Light
        traffic_light_instance = Traffic_Light()
        
        # Input parameters
        color1 = "red"
        coordinates1 = [0.6, 0.5, 0.7, 0.6]

        
        # Call the TL_Logic method and get the result
        speed, distance = traffic_light_instance.TL_Logic(color1, coordinates1)
        
        # Assert the expected behavior
        self.assertEqual(speed, 69)
        #self.assertEqual(distance, expected_distance)

    def test_TL_Logic_green(self):
        # Instantiate Traffic_Light
        traffic_light_instance = Traffic_Light()
        
        # Input parameters
        color1 = "green"
        coordinates1 = [0.6, 0.5, 0.7, 0.6]
        
        # Call the TL_Logic method and get the result
        speed, distance = traffic_light_instance.TL_Logic(color1, coordinates1)
        
        # Assert the expected behavior
        self.assertEqual(speed, 100)
        #self.assertEqual(distance, expected_distance)
if __name__ == '__main__':
    unittest.main()
