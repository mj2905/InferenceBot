import logging
import urllib.request as urllib

from bs4 import BeautifulSoup

from DataStructures.Datastructs import *
from Wiki import WikiStrings

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

baseUrl = 'http://wikipast.epfl.ch/wikipast/index.php/'
listPage = 'InferenceBot_page_test_-_Secundinus_Aurelianus'


def scrap_generic(data, scrapper):
    """
    Function for scrapping a concept from a Wikipast page. It does not rely on a particular page layout.
    Instead, it looks for occurrences of the concept keyword (as defined by the scrapper object) and extracts 
    objects from the corresponding lines.
    
    :param data: The source code from a wiki page.
    :param scrapper: The Scrapper class which parametrize how the actual object extraction is done.
    :return: A set of objects corresponding to the concept scrapped.
    """
    scrappedSet = set()
    entities = scrapper.find(data)

    logging.info("The scrapper found %d candidate entries for %s", len(entities), scrapper.keyword())
    for candidate in entities:
        tag = candidate.parent.parent
        candidateStr = tag.text
        logging.debug("Candidate for %s is %s", scrapper.keyword(), candidateStr)

        scrappedEntity = scrapper.extract(str(candidateStr))

        logging.info("Crafted object: %s", str(scrappedEntity))

        scrappedSet.add(scrappedEntity)

    return scrappedSet


class Scrapper(metaclass=ABCMeta):
    """
    Abstract class which defines the blueprint for a Scrapper object
    """

    @staticmethod
    @abstractmethod
    def keyword():
        """
        :return: The keyword describing which concept to scrap 
        """
        pass

    @staticmethod
    @abstractmethod
    def find(data):
        """
        :param data: The source code from a Wiki page.
        :return: A list of all the tags that match the concept
        """
        pass

    @staticmethod
    @abstractmethod
    def extract(s):
        """
        :param s: The string entry from which to extract an encounter
        :return: An object matching the concept if it was possible to extract one, None otherwise.
        """
        pass


class BirthScrapper(Scrapper):
    """
    A Scrapper object specialized in scrapping births of individuals
    """

    @staticmethod
    def keyword():
        return WikiStrings.BIRTH

    @staticmethod
    def find(data):
        return data.findAll(string=WikiStrings.BIRTH)

    @staticmethod
    def extract(s):
        """      
        The usual birth format is the following:

        1234.56.78 / Location. Naissance de X.

        The line is first split at '/' to retrieve the date, then at the first dot to retrieve the location and
        finally splits the remaining string at each space. The resulting list is filtered according to the list of 
        words to discard as given in the WikiStrings file and the Birth object is created with the remaining data.
        This data is assumed to be the first and last name of an individual, nothing more, nothing less. If the 
        remaining data does not math the format expected it is discarded and the entry is logged.

        :param s: The string entry from which to extract a birth
        :return: An Birth object if it was possible to extract one, None otherwise.
        """
        # Remove trailing dot
        if s.endswith("."):
            s = s[:-1]

        (date, locAndBirth) = s.split("/")
        (location, person) = locAndBirth.split(".", 1)  # Specify at most 1 split to retrieve location

        # Extract only people's names
        person = person.strip().split(" ")
        person = [x for x in person if x not in WikiStrings.BIRTH_TODISCARD]

        if (len(person) != 2):
            logging.warning("The scrapper discarded a candidate birth because it " +
                            "did not have the correct number of names in it. " +
                            "The discarded entry is %s", s)
            return None

        p1 = Person(person[0], person[1])
        d = Date.extractDate(date)
        l = Location(location)

        return Birth(d, l, p1)


class EncounterScrapper(Scrapper):
    """
    A Scrapper object specialized in scrapping encounter between two individuals
    """

    @staticmethod
    def keyword():
        return WikiStrings.ENCOUNTER

    @staticmethod
    def find(data):
        return data.findAll(string=WikiStrings.ENCOUNTER)

    @staticmethod
    def extract(s):
        """      
        The usual encounter format is the following:
        
        1234.56.78 / LocationCity. Rencontre de A avec B.
        
        The line is first split at '/' to retrieve the date, then at the first dot to retrieve the location and
        finally splits the remaining string at each space. The resulting list is filtered according to the list of 
        words to discard as given in the WikiStrings file and the Encounter object is created with the remaining data.
        This data is assumed to be the first and last name of both protagonists, nothing more, nothing less. If the 
        remaining data does not math the format expected it is discarded and the entry is logged.
        
        :param s: The string entry from which to extract an encounter
        :return: An encounter object if it was possible to extract one, None otherwise.
        """
        # Remove trailing dot
        if (s.endswith(".")):
            s = s[:-1]

        (date, locAndPeople) = s.split("/")
        (location, people) = locAndPeople.split(".", 1)  # Specify at most 1 split to retrieve location

        # Extract only people's names
        people = people.strip().split(" ")
        people = [x for x in people if x not in WikiStrings.ENCOUNTER_TODISCARD]

        if (len(people) != 4):
            logging.warning("The scrapper discarded a candidate encounter because it " +
                            "did not have the correct number of names in it. " +
                            "The discarded entry is %s", s)
            return None

        p1 = Person(people[0], people[1])
        p2 = Person(people[2], people[3])
        d = Date.extractDate(date)
        return Encounter(d, p1, p2)

def run():
    response = urllib.urlopen(baseUrl + listPage)
    pageSource = response.read()
    soup = BeautifulSoup(pageSource, 'lxml')
    scrap_generic(soup, BirthScrapper)
    scrap_generic(soup, EncounterScrapper)

if __name__ == '__main__':
    run()
