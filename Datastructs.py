from abc import ABCMeta, abstractmethod

from Motor.Predicate import Atom, Predicate


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


class Person(Atomiseable):
    """
    Stores the data associated with an individual
    """

    def __init__(self, name, lastname):
        self.name = name
        self.lastname = lastname

    def __str__(self):
        return self.name + " " + self.lastname

    def toAtom(self):
        return Atom(self.name + " " + self.lastname, False)


class Location(Atomiseable):
    """
    Stores the data associated with a location
    """

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

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

    def __str__(self):
        return "{y}.{m}.{d} - {h}:{min}:{s}".format(
            y=self.year, m=self.month, d=self.day,
            h=self.hour, min=self.minute, s=self.second
        )

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

    def __str__(self):
        return str(self.date) + " / Naissance de " + str(self.person)

    def toPredicate(self):
        return Predicate([self.person.toAtom(), self.date.toAtom()], "birth")


class Encounter(Event):
    def __init__(self, date, person1, person2):
        super().__init__(date)
        self.person1 = person1
        self.person2 = person2

    def __str__(self):
        return str(self.date) + " - Rencontre de " + str(self.person1) + " et " + str(self.person2)

    def toPredicate(self):
        return Predicate([self.person1.toAtom(), self.person2.toAtom()], "encounter")


def main():
    p = Person("Foo", "Bar")
    b = Birth(Date(1980), p)
    print(p)
    print(p.toAtom())
    print(b)
    print(b.toPredicate())


if __name__ == '__main__':
    main()
