import unittest

from DataStructures.Datastructs import *


class TestDate(unittest.TestCase):
    def setUp(self):
        self.d1 = Date(1, 2, 3, 4, 5, 6)
        self.d2 = Date(1, 2, 3, 4, 5, 6)

    def test_constructor(self):
        self.assertEqual(self.d1.year, 1)
        self.assertEqual(self.d1.month, 2)
        self.assertEqual(self.d1.day, 3)
        self.assertEqual(self.d1.hour, 4)
        self.assertEqual(self.d1.minute, 5)
        self.assertEqual(self.d1.second, 6)

    def test_hash(self):
        self.assertEqual(hash(self.d1), hash(self.d2))

    def test_eq(self):
        self.assertEqual(self.d1, self.d2)

    def test_extractDate(self):
        self.assertEqual(Date.extractDate("01.02.03 - 04:05:06"), self.d1)
        self.assertEqual(Date.extractDate("01.02.03"), Date(1, 2, 3))


if __name__ == '__main__':
    unittest.main()
