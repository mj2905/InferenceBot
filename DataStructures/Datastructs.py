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

    def __hash__(self):
        return hash(self.__key())

    def toAtom(self):
        return Atom(self.name, False)


class Date(Atomiseable):
    """
    Custom Date class which can be easily be converted into an Atom usable by the inference engine
    """

    def __init__(self, year, month=1, day=1, hour=0, minute=0, second=0):
        self.year = int(year)
        self.month = int(month)
        self.day = int(day)
        self.hour = int(hour)
        self.minute = int(minute)
        self.second = int(second)

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

    def isBefore(self, other):
        return (self.year, self.month, self.day) < (other.year, other.month, other.day)

    def isBeforePredicate(self, other):
        before = "avant"
        if self.isBefore(other):
            return Predicate([self.toAtom(), other.toAtom()], before)
        else:
            return Predicate([other.toAtom(), self.toAtom()], before)


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


class LifeEvent(Event, metaclass=ABCMeta):
    def __init__(self, date, location, person, strName, predicateName=None):
        super(LifeEvent, self).__init__(date)
        self.location = location
        self.person = person
        self.strName = strName
        if predicateName is None:
            predicateName = strName
        self.predicateName = predicateName

    def __key(self):
        return (self.date, self.location, self.person)

    def __str__(self):
        return str(self.date) + " / " + str(self.location) + ". " + self.strName + " de " + str(self.person) + "."

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return self.__key() == other.__key()

    def toPredicate(self):
        return Predicate([self.date.toAtom(), self.location.toAtom(), self.person.toAtom()], self.predicateName)


class Birth(LifeEvent):
    def __init__(self, date, location, person):
        super(Birth, self).__init__(date, location, person, "Naissance")


class Death(LifeEvent):
    def __init__(self, date, location, person):
        super(Death, self).__init__(date, location, person, "Mort")


class Encounter(Event):
    def __init__(self, date, person1, person2):
        super().__init__(date)
        self.person1 = person1
        self.person2 = person2

    def __key(self):
        return (self.date, self.person1, self.person2)

    def __str__(self):
        return str(self.date) + " - Rencontre de " + str(self.person1) + " et " + str(self.person2) + "."

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return self.__key() == other.__key()

    def toPredicate(self):
        return Predicate([self.person1.toAtom(), self.person2.toAtom()], "encounter")


def main():
    pass


if __name__ == '__main__':
    main()
