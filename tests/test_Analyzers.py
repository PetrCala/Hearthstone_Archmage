import unittest
from pyscripts import DataExtractor, DataProcessor

P = DataProcessor.DataProcessor()
E = DataExtractor.DataExtractor()

class test_Analyzers(unittest.TestCase):
    def test_DP_percentage_to_float(self):
        x = P.percentage_float('42.69%', P2F = True)
        self.assertEqual(x, 0.4269, 'Percentage to float is not working correctly.')

    def test_DP_float_to_percentage(self):
        x = P.percentage_float(0.4269, P2F = False)
        self.assertEqual(x, '42.69%', 'Float to percentage is not working correctly.')


if __name__ == '__main__':
    unittest.main()