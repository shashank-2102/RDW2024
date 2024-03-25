import unittest
from Pedestrian_Manoeuvre import Pedestrian_Maneouvre
from RT import RT

class PD_Logic_Test(unittest.TestCase):
    
    def test_PD_Logic_no_pedestrian(self):
        # Instantiate Pedestrian
        Pedestrian_instance = Pedestrian_Maneouvre()
        
        # Input parameters
        coordinates1 = [0.4, 0.5, 0.7, 0.6]
        
        # Call the PD_check method and get the result
        result1 = Pedestrian_instance.pedestrian_check(coordinates1)
        result2 = True
        result3 = True   # When pedestrian isn't found, it doesn't matter if there is pedestrian sign or crossing
        
        # Assert the expected behavior
        self.assertEqual(Pedestrian_instance.pedestrian_logic(result1, result2, result3), [50, 0]) #set correct value

    def test_PD_Logic_PD_and_PD_sign(self):
        # Instantiate Pedestrian
        Pedestrian_instance = Pedestrian_Maneouvre()
        
        # Input parameters
        coordinates1 = [0.6, 0.5, 0.7, 0.6] # distance for pedestrian
        coordinates2 = [0.6, 0.5, 0.7, 0.6] # distance for pedestrian sign
        
        # Call the PD_check method and get the result
        result1 = Pedestrian_instance.pedestrian_check(coordinates1)
        result2 = Pedestrian_instance.pedestrian_sign_check(coordinates2)
        result3 = True   # When pedestrian and sign are found, set speed 0
        
        self.assertEqual(Pedestrian_instance.pedestrian_logic(result1, result2, result3), [0, 0]) #set correct value
    
    def test_PD_Logic_PD_and_PD_crossing(self):
        # Instantiate Pedestrian
        Pedestrian_instance = Pedestrian_Maneouvre()
        
        # Input parameters
        coordinates1 = [0.6, 0.5, 0.7, 0.6] # distance for pedestrian
        coordinates3 = [0.6, 0.5, 0.7, 0.6] # distance for pedestrian crossing
        
        # Call the PD_check method and get the result
        result1 = Pedestrian_instance.pedestrian_check(coordinates1)
        result2 = True
        result3 = Pedestrian_instance.pedestrian_crossing_check(coordinates3)
        
        self.assertEqual(Pedestrian_instance.pedestrian_logic(result1, result2, result3), [0, 0]) #set correct value
        
if __name__ == '__main__':
    unittest.main()