import unittest
from Logic_Thread.Maneouvres.Pedestrian_Manoeuvre import Pedestrian_Maneouvre
#from RDWLogic.RT import RT

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
        
        # Call the PD_logic method and get the result
        speed, distance = Pedestrian_instance.pedestrian_logic(result1, result2, result3)
        
        # Assert the expected behavior
        self.assertEqual(speed, 50)
        #self.assertEqual(distance, expected_distance)

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
        
        # Call the PD_logic method and get the result
        speed, distance = Pedestrian_instance.pedestrian_logic(result1, result2, result3)
        
        # Assert the expected behavior
        self.assertEqual(speed, 0)
        #self.assertEqual(distance, expected_distance)
    
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
        
        # Call the PD_logic method and get the result
        speed, distance = Pedestrian_instance.pedestrian_logic(result1, result2, result3)
        
        # Assert the expected behavior
        self.assertEqual(speed, 0)
        #self.assertEqual(distance, expected_distance)
        
if __name__ == '__main__':
    unittest.main()