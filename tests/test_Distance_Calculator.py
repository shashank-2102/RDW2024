import unittest
from Distance_Calculator import Calculate_area

class TestCalculateArea(unittest.TestCase):
    def test_traffic_light(self):
        object = ['traffic light', 0, 0, 10, 10]
        expected_area = (10-0)*(10-0)/(0.3*0.1)
        self.assertEqual(Calculate_area(object), [expected_area, 'traffic light'])

    def test_speed_sign(self):
        object = ['speed sign', 0, 0, 5, 5]
        expected_area = (5-0)*(5-0)/(0.6*0.6)
        self.assertEqual(Calculate_area(object), [expected_area, 'speed sign'])

    def test_zebra_crossing(self):
        object = ['zebra crossing', 0, 0, 20, 10]
        expected_area = (20-0)*(10-0)/(2*3)
        self.assertEqual(Calculate_area(object), [expected_area, 'zebra crossing'])

    def test_other_object(self):
        object = ['unknown object', 0, 0, 5, 5]
        expected_area = None
        self.assertEqual(Calculate_area(object), [expected_area, 'unknown object'])

if __name__ == '__main__':
    unittest.main()
