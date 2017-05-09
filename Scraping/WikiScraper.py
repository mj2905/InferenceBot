import logging
import threading
import urllib.request as urllib

from bs4 import BeautifulSoup

from DataStructures.Datastructs import *
from DataStructures.Datastructs import WikiData
from Scraping import WikiStrings
from Scraping.WikiStrings import translationTable


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
        :param s: The string entry from which to extract a concept
        :return: An object matching the concept if it was possible to extract one, None otherwise.
        """
        pass

    @staticmethod
    def unaryEventExtractor(s, stringsToDiscard, eventName):
        """
        The usual unary event format is the following:

        Date / Location. Event X [for/from/of] Person Y.

        The line is first split at '/' to retrieve the date, then at the first dot to retrieve the location and
        finally splits the remaining string at each space. The resulting list is filtered according to the list of
        words to discard as given in the WikiStrings file and the event object is created with the remaining data.
        If the remaining data does not math the format expected it is discarded and the entry is logged.

        :param s: The string entry from which to extract the event.
        :param stringsToDiscard: The constant list of string to discard from the event entry.
        :param eventName: The name of the event. (For logging purposes)
        :return: A tuple (Date, Location, Person) which can be used to create the event
        """
        BAD_FORMAT = ''.join(
            ["The scraper discarded a candidate ", eventName,
             " because it did not have the correct format. ",
             "The discarded entry is %s"])

        if s.endswith("."):
            s = s[:-1]

        dateRes = s.split("/")

        if len(dateRes) != 2:
            logging.warning(BAD_FORMAT, s)
            return None

        date, locAndEvent = dateRes[0], dateRes[1]
        locRes = locAndEvent.split(".", 1)  # Specify at most 1 split to retrieve location

        if (len(locRes) < 2):
            logging.warning(BAD_FORMAT, s)
            return None

        location, person = locRes[0], locRes[1]

        # Extract only people's names
        # person = person.translate(translationTable).strip().split(" ")
        # person = [x for x in person if x not in stringsToDiscard]
        person = re.sub(stringsToDiscard, '', person).split(" ")
        person = [x for x in person if x != '']

        if (len(person) < 2):
            logging.warning(BAD_FORMAT, s)
            return None

        p = Person(person[0], person[1])
        d = Date.extractDate(date)
        l = Location(location)

        return d, l, p

    @staticmethod
    def binaryEventExtractor(s, stringsToDiscard, eventName):
        """
        The usual binary event format is the following:

        Date / Location. Event X [for/from/of] Person Y [with/and] Person Z.

        The line is first split at '/' to retrieve the date, then at the first dot to retrieve the location and
        finally splits the remaining string at each space. The resulting list is filtered according to the list of
        words to discard as given in the WikiStrings file and the event object is created with the remaining data.
        If the remaining data does not math the format expected it is discarded and the entry is logged.

        :param s: The string entry from which to extract the event.
        :param stringsToDiscard: The constant list of string to discard from the event entry.
        :param eventName: The name of the event. (For logging purposes)
        :return: A tuple (Date, Location, Person1, Person2) which can be used to create the event
        """
        BAD_FORMAT = ''.join(
            ["The scraper discarded a candidate ", eventName,
             " because it did not have the correct format. ",
             "The discarded entry is %s"])

        if (s.endswith(".")):
            s = s[:-1]

        dateRes = s.split("/")

        if (len(dateRes) != 2):
            logging.warning(BAD_FORMAT, s)
            return None

        date, locAndPeople = dateRes[0], dateRes[1]

        locRes = locAndPeople.split(".", 1)  # Specify at most 1 split to retrieve location

        if (len(locRes) < 2):
            logging.warning(BAD_FORMAT, s)
            return None

        location, people = locRes[0], locRes[1]

        # Extract only people's names. The translation removes unwanted characters from the string
        people = people.translate(translationTable).strip().split(" ")
        people = [x for x in people if x not in stringsToDiscard]

        if (len(people) < 4):
            logging.warning(BAD_FORMAT, s)
            return None

        p1 = Person(people[0], people[1])
        p2 = Person(people[2], people[3])
        d = Date.extractDate(date)
        l = Location(location)

        return d, l, p1, p2


class BirthScraper(Scraper):
    """
    A Scraper class specialized in scraping births of individuals
    """

    @staticmethod
    def keyword():
        return WikiStrings.BIRTH

    @staticmethod
    def find(data):
        return data.findAll(string=WikiStrings.BIRTH)

    @staticmethod
    def extract(s):
        tmp = Scraper.unaryEventExtractor(s, WikiStrings.BIRTH_TODISCARD, WikiStrings.BIRTH)
        return None if tmp is None else Birth(*tmp)


class DeathScraper(Scraper):
    """
    A Scraper class specialized in scraping deaths of individuals
    """

    @staticmethod
    def keyword():
        return WikiStrings.DEATH

    @staticmethod
    def find(data):
        return data.findAll(string=WikiStrings.DEATH)

    @staticmethod
    def extract(s):
        tmp = Scraper.unaryEventExtractor(s, WikiStrings.DEATH_TODISCARD, WikiStrings.DEATH)
        return None if tmp is None else Death(*tmp)


class PositionScraper(Scraper):
    """
    A Scraper class specialized in scraping births of individuals
    """

    @staticmethod
    def keyword():
        return WikiStrings.POSITION

    @staticmethod
    def find(data):
        return data.findAll(string=WikiStrings.POSITION) \
            # +data.findAll(string=WikiStrings.DEATH)+ data.findAll(string=WikiStrings.BIRTH)

    @staticmethod
    def extract(s):
        tmp = Scraper.unaryEventExtractor(s, WikiStrings.POSITION_TODISCARD, WikiStrings.POSITION)
        return None if tmp is None else Position(*tmp)


class EncounterScraper(Scraper):
    """
    A Scraper class specialized in scraping encounter between two individuals
    """

    @staticmethod
    def keyword():
        return WikiStrings.ENCOUNTER

    @staticmethod
    def find(data):
        return data.findAll(string=WikiStrings.ENCOUNTER)

    @staticmethod
    def extract(s):
        tmp = Scraper.binaryEventExtractor(s, WikiStrings.ENCOUNTER_TODISCARD, WikiStrings.ENCOUNTER)
        return None if tmp is None else Encounter(*tmp)

class ElectionScraper(Scraper):
    """
    A Scapper class psecialized in scrapping elections of individuals
    """

    @staticmethod
    def keyword():
        return WikiStrings.ELECTION

    @staticmethod
    def find(data):
        return data.findAll(string=WikiStrings.ELECTION)

    @staticmethod
    def extract(s):
        tmp = Scraper.unaryEventExtractor(s, WikiStrings.ELECTION_TODISCARD, WikiStrings.ELECTION)
        return None if tmp is None else Election(*tmp)


def processUrl(url, responses, i):
    tmp = None
    try:
        tmp = urllib.urlopen(url)
    except:
        logging.error("The following url threw an error: %s", url)
        return

    if tmp.getcode() != 200:
        logging.error("The following url could not be reached: %s", url)

    responses[i] = tmp


def run(urlList):
    resData = WikiData()
    responses = [None] * len(urlList)
    processes = []

    for i in range(len(urlList)):
        process = threading.Thread(target=processUrl, args=[urlList[i], responses, i])
        process.setDaemon(True)
        process.start()
        processes.append(process)

    for process in processes:
        process.join()

    for response in responses:
        if response is None:
            continue

        pageSource = response.read()
        soup = BeautifulSoup(pageSource, 'lxml')
        births = scrap_generic(soup, BirthScraper)
        deaths = scrap_generic(soup, DeathScraper)
        encounters = scrap_generic(soup, EncounterScraper)
        positions = scrap_generic(soup, PositionScraper)
        elections = scrap_generic(soup, ElectionScraper)

        resData.addData(deaths, births, encounters, positions, elections)

    return resData


if __name__ == '__main__':
    run()

