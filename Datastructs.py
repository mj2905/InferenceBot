from abc import ABCMeta, abstractmethod

from InferenceEngine.Predicate import Atom, Predicate


class Atomiseable(metaclass=ABCMeta):
    """
    Abstract class that provides a function for converting the object into 
    an Atom which can then be parsed by the inference engine
    """

    @abstractmethod
    def toAtom(self):
        pass


class Predicateable(metaclass=ABCMeta):
    """
    Abstract class that provides a function for converting the object into
    a Predicate which can then be parsed by the inference engine
    """

    @abstractmethod
    def toPredicate(self):
        pass

    def __hash__(self):
        return hash(self.__key())


class Person(Atomiseable):
    """
    Stores the data associated with an individual
    """

    def __init__(self, name, lastname):
        self.name = name
        self.lastname = lastname

    def __key(self):
        return (self.name, self.lastname)

    def __str__(self):
        return self.name + " " + self.lastname

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return self.__key() == other.__key()

    def toAtom(self):
        return Atom(self.name + " " + self.lastname, False)


class Location(Atomiseable):
    """
    Stores the data associated with a location
    """

    def __init__(self, name):
        self.name = name

    def __key(self):
        return (self.name)

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.__key() == other.__key()

    def toAtom(self):
        return Atom(self.name, False)


class Date(Atomiseable):
    """
    Custom Date class which can be easily be converted into an Atom usable by the inference engine
    """

    def __init__(self, year, month=1, day=1, hour=0, minute=0, second=0):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second

    def __key(self):
        return (self.year, self.month, self.day, self.hour, self.minute, self.second)

    def __str__(self):
        return "{y}.{m}.{d} - {h}:{min}:{s}".format(
            y=self.year, m=self.month, d=self.day,
            h=self.hour, min=self.minute, s=self.second
        )

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return self.__key() == other.__key()

    @staticmethod
    def extractDate(str):
        s = str.strip()
        l = s.split("-")
        datelen = len(l)

        if datelen == 1:
            (y, m, d) = l[0].split(".")
            return Date(y, m, d)
        elif datelen == 2:
            (y, m, d) = l[0].strip().split(".")
            (h, min, s) = l[1].strip().split(":")
            return Date(y, m, d, h, min, s)

        raise ValueError("Date extraction only works with either YYYY.MM.DD or YYYY.MM.DD - HH.MM.SS")


    def toAtom(self):
        return Atom(str(self), False)


class Event(Predicateable):
    """
    Stores the data about a historical event.
    """

    def __init__(self, date):
        """

        :param date: The date at which the event occurred
        """
        self.date = date

    def __str__(self):
        return str(self.date)

    @abstractmethod
    def toPredicate(self):
        pass


class Birth(Event):
    def __init__(self, date, person):
        super().__init__(date)
        self.person = person

    def __key(self):
        return (self.date, self.person)

    def __str__(self):
        return str(self.date) + " / Naissance de " + str(self.person)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return self.__key() == other.__key()

    def toPredicate(self):
        return Predicate([self.person.toAtom(), self.date.toAtom()], "birth")


class Encounter(Event):
    def __init__(self, date, person1, person2):
        super().__init__(date)
        self.person1 = person1
        self.person2 = person2

    def __key(self):
        return (self.date, self.person1, self.person2)

    def __str__(self):
        return str(self.date) + " - Rencontre de " + str(self.person1) + " et " + str(self.person2)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return self.__key() == other.__key()

    def toPredicate(self):
        return Predicate([self.person1.toAtom(), self.person2.toAtom()], "encounter")


def main():
    p1 = Person("Foo1", "Bar1")
    p2 = Person("Foo2", "Bar2")

    print(hash(p1))
    print(hash(p2))

    b = Birth(Date(1980), p1)
    e1 = Encounter(Date(1980), p1, p2)
    e2 = Encounter(Date(1980), p1, p2)

    print(hash(e1))
    print(hash(e2))

    print(b.toPredicate())
    print(Date.extractDate("2017.02.02"))
    print(Date.extractDate("2017.02.02 - 01:01:01"))

    d1 = Date(2017, 2, 2, 1, 1, 1)
    d2 = Date(2017, 2, 2, 1, 1, 1)

    print(d1 == d2)

    print(hash(d1))
    print(hash(d2))


if __name__ == '__main__':
    main()
