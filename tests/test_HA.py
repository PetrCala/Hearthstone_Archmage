import unittest
from pyscripts import HearthstoneArchmage

H = HearthstoneArchmage.GraphicalArchmage()

class test_Analyzers(unittest.TestCase):
    def test1(self):
        self.assertEqual(sum([1,2,3]), 6, 'Should be 6')

if __name__ == '__main__':
    unittest.main()