import re
from abc import ABCMeta, abstractmethod

from InferenceEngine.Predicate import Atom, Predicate
from Scraping.WikiStrings import dateTranslationTable


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
    def toPredicate(self, url):
        self.url = url
        pass

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

    # TODO: Change this method
    def isFar(self, other):
        return self != other

    def isFarPredicate(self, other):
        far = "loin"
        if self.isFar(other):
            return Predicate([self.toAtom(), other.toAtom()], far)


class Date(Atomiseable):
    """
    Custom Date class which can be easily be converted into an Atom usable by the inference engine
    """

    def __init__(self, year=0, month=0, day=0, hour=0, minute=0, second=0):
        print(year)
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
        vals = list()
        s = str.translate(dateTranslationTable).strip()

        while (len(s) > 0 and len(vals) < 6):
            i = re.search("[\.:-]", s)
            if i:
                tmp = s[:i.start()]
                s = s[i.start() + 1:].strip()
            else:
                tmp = s
                s = ''
            vals.append(tmp)
        return Date(*tuple(vals))

    def toAtom(self):
        return Atom(str(self), False)

    def isBefore(self, other):
        return (self.year, self.month, self.day) < (other.year, other.month, other.day)

    def isDifferent(self, other):
        return (self.year, self.month, self.day) != (other.year, other.month, other.day)

    def isBeforePredicate(self, other):
        before = "avant"
        if self.isBefore(other):
            return Predicate([self.toAtom(), other.toAtom()], before)
        else:
            return Predicate([other.toAtom(), self.toAtom()], before)

    def isDifferentPredicate(self, other):
        different = "different"
        same = "same"
        if self.isDifferent(other):
            return Predicate([self.toAtom(), other.toAtom()], different)
        else:
            return Predicate([self.toAtom(), other.toAtom()], same)


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
    def toPredicate(self, url):
        super(Event, self).toPredicate(url)
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

    def toPredicate(self, url):
        return Predicate([self.date.toAtom(), self.location.toAtom(), self.person.toAtom()], self.predicateName, {url})

class SocialEvent(Event, metaclass=ABCMeta):
    def __init__(self, date, location, person1, person2, strName, predicateName=None):
        super(SocialEvent, self).__init__(date)
        self.location = location
        self.person1 = person1
        self.person2 = person2
        self.strName = strName
        if predicateName is None:
            predicateName = strName
        self.predicateName = predicateName

    def __key(self):
        return (self.date, self.location, hash(self.person1) ^ hash(self.person2))

    def __str__(self):
        return str(self.date) + " - " + self.strName + " de " + str(self.person1) + " et " + str(self.person2) + "."

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return self.__key() == other.__key()

    def toPredicate(self, url):
        return Predicate([self.date.toAtom(), self.location.toAtom(), self.person1.toAtom(), self.person2.toAtom()],
                         self.predicateName, {url})


class Birth(LifeEvent):
    def __init__(self, date, location, person):
        super(Birth, self).__init__(date, location, person, "Naissance")


class Death(LifeEvent):
    def __init__(self, date, location, person):
        super(Death, self).__init__(date, location, person, "Mort")


class Position(LifeEvent):
    def __init__(self, date, location, person):
        super(Position, self).__init__(date, location, person, "Position")


class Election(LifeEvent):
    def __init__(self, date, location, person):
        super(Election, self).__init__(date, location, person, "Election")

class Encounter(SocialEvent):
    def __init__(self, date, location, person1, person2):
        super(Encounter, self).__init__(date, location, person1, person2, "Rencontre")

class Mariage(SocialEvent):
    def __init__(self, date, location, person1, person2):
        super(Mariage, self).__init__(date, location, person1, person2, "Mariage")

def main():
    pass


if __name__ == '__main__':
    main()


class WikiData:
    def __init__(self):
        self.data = set()

    def addPages(self, that):
        self.data |= that

    def joinWith(self, that):
        self.data |= that.data

    def add(self, elem):
        self.data.add(elem)



class WikiPage:
    def __init__(self, url):
        self.deaths = set()
        self.births = set()
        self.encounters = set()
        self.positions = set()
        self.elections = set()
        self.weddings = set()
        self.url = url

    def addData(self, deaths, births, encounters, positions, elections, weddings, divorces):
        self.deaths |= deaths
        self.births |= births
        self.encounters |= encounters
        self.positions |= positions
        self.elections |= elections
        self.weddings |= weddings

    def __str__(self):
        resStr = []

        for death in self.deaths:
            resStr.append(str(death))
        for births in self.births:
            resStr.append(str(births))
        for encounters in self.encounters:
            resStr.append(str(encounters))
        for positions in self.positions:
            resStr.append(str(positions))
        for elections in self.elections:
            resStr.append(str(elections))
        for wedding in self.weddings:
            resStr.append(str(wedding))

        return '\n'.join(resStr)
