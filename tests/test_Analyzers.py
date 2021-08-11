import unittest
import pandas as pd
from pyscripts import DataExtractor, DataProcessor

P = DataProcessor.DataProcessor()
E = DataExtractor.DataExtractor()

class test_Analyzers(unittest.TestCase):
    def test_DP_percentage_to_float(self):
        '''Test whether the DP.percentage_to_float method converts a string
        in a percentage format to a float.
        '''
        x = P.percentage_float('42.69%', P2F = True)
        self.assertEqual(x, 0.4269, 'Percentage to float is not working correctly.')

    def test_DP_float_to_percentage(self):
        '''Test whether DP.float_to_percentage method converts
        a float input to percentage.
        '''
        x = P.percentage_float(0.4269, P2F = False)
        self.assertEqual(x, '42.69%', 'Float to percentage is not working correctly.')

    def test_DP_path_format(self):
        '''Test whether the path specified in DP.card_data_to_excel contains
        a '/' sign.
        '''
        x = P.card_data_to_excel(date = '07-09', processed = True,
                deck = 'Rogue - Miracle Rogue', WR_against = ['Mage', 'Rogue'],
                test_path = True)
        self.assertNotIn('/', x, 'The path format is generated incorrectly.')

    def test_DP_analyze_winrates(self):
        '''Test whether the output that DP.analyze_winrates returns
        is a pandas data frame.
        '''
        x = P.analyze_deck_winrates(date = '07-09',
            deck = 'Rogue - Miracle Rogue', WR_against = ['maGe', 'ROGUE'])
        self.assertIsInstance(x, pd.DataFrame, 'The output is not a pandas data frame.')
        
if __name__ == '__main__':
    unittest.main()