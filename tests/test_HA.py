import unittest
import pandas as pd
from pyscripts import HearthstoneArchmage

H = HearthstoneArchmage.GraphicalArchmage()

class test_Analyzers(unittest.TestCase):
    def test_generate_class_elements(self):
        temp = H.generate_class_elements(el_type = 'Checkbox',
            key_tag = 'DE', group_tag = 'de_sel_1', size = (10,1),
            enable_events = False, start = 1, end = 10) 
        self.assertEqual(type(temp), list, 'Should be a list')

if __name__ == '__main__':
    unittest.main()