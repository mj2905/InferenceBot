import logging
import urllib.request as urllib

from bs4 import BeautifulSoup

from DataStructures.Datastructs import *
from Scraping import WikiStrings
from Scraping.WikiStrings import translationTable

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)


# Specify characters that could potentially make an entry unreadable and that should therefore be removed


def scrap_generic(data, scraper):
    """
    Function for scraping a concept from a Wikipast page. It does not rely on a particular page layout.
    Instead, it looks for occurrences of the concept keyword (as defined by the scraper object) and extracts 
    objects from the corresponding lines.
    
    :param data: The source code from a wiki page.
    :param scraper: The Scraper class which parametrize how the actual object extraction is done.
    :return: A set of objects corresponding to the concept scraped.
    """
    scrapedSet = set()
    entities = scraper.find(data)

    logging.debug("The scraper found %d candidate entries for %s", len(entities), scraper.keyword())
    for candidate in entities:
        tag = candidate.parent.parent
        candidateStr = str(tag.text)
        logging.debug("Candidate for %s is %s", scraper.keyword(), candidateStr)

        scrapedEntity = scraper.extract(candidateStr)

        logging.info("Crafted object: %s", str(scrapedEntity))

        scrapedSet.add(scrapedEntity)

    return scrapedSet


class Scraper(metaclass=ABCMeta):
    """
    Abstract class which defines the blueprint for a Scraper object
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


class BirthScraper(Scraper):
    """
    A Scraper object specialized in scraping births of individuals
    """
    BAD_FORMAT = ''.join(
        ["The scraper discarded a candidate birth because it ",
         "did not have the correct format. ",
         "The discarded entry is: %s"])

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

        dateRes = s.split("/")

        if (len(dateRes) != 2):
            logging.warning(BirthScraper.BAD_FORMAT, s)
            return None

        date, locAndBirth = dateRes[0], dateRes[1]

        locRes = locAndBirth.split(".", 1)  # Specify at most 1 split to retrieve location

        if (len(locRes) != 2):
            logging.warning(BirthScraper.BAD_FORMAT, s)
            return None

        location, person = locRes[0], locRes[1]

        # Extract only people's names. The translation removes unwanted chars from the remaining string
        person = person.translate(translationTable).strip().split(" ")
        person = [x for x in person if x not in WikiStrings.BIRTH_TODISCARD]

        if (len(person) < 2):
            logging.warning(BirthScraper.BAD_FORMAT, s)
            return None

        p1 = Person(person[0], person[1])
        d = Date.extractDate(date)
        l = Location(location)

        return Birth(d, l, p1)


class EncounterScraper(Scraper):
    """
    A Scraper object specialized in scraping encounter between two individuals
    """
    BAD_FORMAT = ''.join(
        ["The scraper discarded a candidate encounter because it ",
         "did not have the correct format. ",
         "The discarded entry is: %s"])

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

        dateRes = s.split("/")

        if (len(dateRes) != 2):
            logging.warning(EncounterScraper.BAD_FORMAT, s)
            return None

        date, locAndPeople = dateRes[0], dateRes[1]

        locRes = locAndPeople.split(".", 1)  # Specify at most 1 split to retrieve location

        if (len(locRes) != 2):
            logging.warning(EncounterScraper.BAD_FORMAT, s)
            return None

        location, people = locRes[0], locRes[1]

        # Extract only people's names. The translation removes unwanted characters from the string
        people = people.translate(translationTable).strip().split(" ")
        people = [x for x in people if x not in WikiStrings.ENCOUNTER_TODISCARD]

        if (len(people) < 4):
            logging.warning(EncounterScraper.BAD_FORMAT, s)
            return None

        p1 = Person(people[0], people[1])
        p2 = Person(people[2], people[3])
        d = Date.extractDate(date)
        return Encounter(d, p1, p2)


def run(urlList):
    resList = list()
    responseList = list()
    for url in urlList:
        try:
            response = urllib.urlopen(url)
        except:
            logging.error("The following url threw an error: %s", url)
            continue

        if response.getcode() != 200:
            logging.error("The following url could not be reached: %s", url)
            continue

        responseList.append(response)

    for response in responseList:
        pageSource = response.read()
        soup = BeautifulSoup(pageSource, 'lxml')
        births = scrap_generic(soup, BirthScraper)
        encounters = scrap_generic(soup, EncounterScraper)
        resList.append([births, encounters])

    return resList

if __name__ == '__main__':
    run()
