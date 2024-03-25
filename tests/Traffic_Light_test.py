import unittest
from Traffic_Light import Traffic_Light
from RT import RT

class TL_Logic_Test(unittest.TestCase):
    traffic_light_instance = Traffic_Light()
    def test_TL_Logic_red(self):
        # Instantiate Traffic_Light
        traffic_light_instance = Traffic_Light()
        
        # Input parameters
        color1 = "red"
        coordinates1 = [0.6, 0.3, 0.7, 0.5] #location is chosen based on the cooordinate statements in the logic
               
        # Assert the expected behavior
        self.assertEqual(traffic_light_instance.TL_Logic(color1, coordinates1), [0, 0.6666666666666666]) #set correct value

    def test_TL_Logic_green(self):
        # Instantiate Traffic_Light
        traffic_light_instance = Traffic_Light()
        
        # Input parameters
        color2 = "green"
        coordinates2 = [0.6, 0.3, 0.7, 0.5]
        
        # Call the TL_Logic method and get the result
        self.assertEqual(traffic_light_instance.TL_Logic(color2, coordinates2), [10, 0.6666666666666666]) #set correct value

if __name__ == '__main__':
    unittest.main()
