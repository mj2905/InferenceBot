import unittest

from DataStructures.Datastructs import *


class TestPerson(unittest.TestCase):
    def setUp(self):
        self.p1 = Person("Foo1", "Bar1")
        self.p2 = Person("Foo2", "Bar2")
        self.p3 = Person("Foo1", "Bar1")
        self.p4 = Person("Foo2", "Bar2")

    def test_hash(self):
        self.assertEqual(hash(self.p1), hash(self.p3))
        self.assertEqual(hash(self.p2), hash(self.p4))

    def test_eq(self):
        self.assertEqual(self.p1, self.p3)
        self.assertEqual(self.p2, self.p4)


class TestLocation(unittest.TestCase):
    def setUp(self):
        self.l1 = Location("Foo1")
        self.l2 = Location("Foo2")
        self.l3 = Location("Foo1")
        self.l4 = Location("Foo2")

    def test_hash(self):
        self.assertEqual(hash(self.l1), hash(self.l3))
        self.assertEqual(hash(self.l2), hash(self.l4))

    def test_eq(self):
        self.assertEqual(self.l1, self.l3)
        self.assertEqual(self.l2, self.l4)


class TestBirth(unittest.TestCase):
    def setUp(self):
        self.d1 = Date(1, 2, 3, 4, 5, 6)
        self.d2 = Date(7, 8, 9, 10, 11, 12)
        self.d3 = Date(1, 2, 3, 4, 5, 6)
        self.d4 = Date(7, 8, 9, 10, 11, 12)
        self.p1 = Person("Foo1", "Bar1")
        self.p2 = Person("Foo2", "Bar2")
        self.p3 = Person("Foo1", "Bar1")
        self.p4 = Person("Foo2", "Bar2")
        self.l1 = Location("Foo1")
        self.l2 = Location("Foo2")

        self.b1 = Birth(self.d1, self.p1, self.l1)
        self.b2 = Birth(self.d2, self.p2, self.l2)
        self.b3 = Birth(self.d3, self.p3, self.l1)
        self.b4 = Birth(self.d4, self.p4, self.l2)

    def test_hash(self):
        self.assertEqual(hash(self.b1), hash(self.b3))
        self.assertEqual(hash(self.b2), hash(self.b4))

    def test_eq(self):
        self.assertEqual(self.b1, self.b3)
        self.assertEqual(self.b2, self.b4)


class TestEncounter(unittest.TestCase):
    def setUp(self):
        self.d1 = Date(1, 2, 3, 4, 5, 6)
        self.d2 = Date(7, 8, 9, 10, 11, 12)
        self.p1 = Person("Foo1", "Bar1")
        self.p2 = Person("Foo2", "Bar2")
        self.p3 = Person("Foo1", "Bar1")
        self.p4 = Person("Foo2", "Bar2")

        self.e1 = Encounter(self.d1, self.p1, self.p2)
        self.e2 = Encounter(self.d2, self.p1, self.p2)
        self.e3 = Encounter(self.d1, self.p3, self.p4)
        self.e4 = Encounter(self.d2, self.p1, self.p2)

    def test_hash(self):
        self.assertEqual(hash(self.e1), hash(self.e3))
        self.assertEqual(hash(self.e2), hash(self.e4))

    def test_eq(self):
        self.assertEqual(self.e1, self.e3)
        self.assertEqual(self.e2, self.e4)


    
class TestDate(unittest.TestCase):
    def setUp(self):
        self.d1 = Date(1, 2, 3, 4, 5, 6)
        self.d2 = Date(1, 2, 3, 4, 5, 6)
        self.d3 = Date(1)

    def test_constructor(self):
        self.assertEqual(self.d3.year, 1)
        self.assertEqual(self.d3.month, 1)
        self.assertEqual(self.d3.day, 1)
        self.assertEqual(self.d3.hour, 0)
        self.assertEqual(self.d3.minute, 0)
        self.assertEqual(self.d3.second, 0)

    def test_hash(self):
        self.assertEqual(hash(self.d1), hash(self.d2))

    def test_eq(self):
        self.assertEqual(self.d1, self.d2)

    def test_extractDate(self):
        self.assertEqual(Date.extractDate("01.02.03 - 04:05:06"), self.d1)
        self.assertEqual(Date.extractDate("01.02.03 - 04"), Date(1, 2, 3, 4))
        self.assertEqual(Date.extractDate("01.02.03"), Date(1, 2, 3))
        self.assertEqual(Date.extractDate("01.02"), Date(1, 2))
        self.assertEqual(Date.extractDate("01"), Date(1))


if __name__ == '__main__':
    unittest.main()
