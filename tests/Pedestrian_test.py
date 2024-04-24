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
        result1 = Pedestrian_instance.person_logic(coordinates1)[0]
        result2 = True
        
        # Assert the expected behavior
        self.assertEqual(Pedestrian_instance.pedestrian_logic(result1, result2), 50) #set correct value
    
    def test_PD_Logic_PD_and_PD_crossing(self):
        # Instantiate Pedestrian
        Pedestrian_instance = Pedestrian_Maneouvre()
        
        # Input parameters
        coordinates1 = [0.6, 0.5, 0.7, 0.6] # distance for pedestrian
        coordinates3 = [0.6, 0.5, 0.7, 0.6] # distance for pedestrian crossing
        
        # Call the PD_check method and get the result
        result1 = Pedestrian_instance.person_logic(coordinates1)[0]
        result2 = Pedestrian_instance.crossing_logic(coordinates3)[0]
        
        self.assertEqual(Pedestrian_instance.pedestrian_logic(result1, result2), 0) #set correct value
        
if __name__ == '__main__':
    unittest.main()