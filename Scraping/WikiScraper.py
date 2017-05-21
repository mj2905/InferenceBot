import logging
import threading
import urllib.request as urllib

from bs4 import BeautifulSoup

from DataStructures.Datastructs import *
from DataStructures.Datastructs import WikiData
from Scraping import WikiStrings
from Scraping.WikiStrings import *

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)


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

        dateRes[0] = dateRes[0].translate(dateTranslationTable).strip()

        if dateRes[0] == '':
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


class BirthScraper(Scraper):
    """
    A Scraper class specialized in scraping births of individuals
    """

    REGEX = r'(?P<date>[0-9]{4}.[0-9]{2}.[0-9]{2}) / (?P<location>[-\w]+). Naissance de (?P<name>[-\w]+) (?P<lastName>[-\w]+).'

    @staticmethod
    def extract(text):
        entities = set()
        result = re.finditer(BirthScraper.REGEX, text)
        for g in result:
            p = Person(g.group('name'), g.group('lastName'))
            d = Date.extractDate(g.group('date'))

            if d is None:
                continue

            l = Location(g.group('location'))

            b = Birth(d, l, p)
            entities.add(b)
            logging.info("Crafted object: %s", b)

        return entities


class DeathScraper(Scraper):
    """
    A Scraper class specialized in scraping deaths of individuals
    """

    REGEX = r'(?P<date>[0-9]{4}.[0-9]{2}.[0-9]{2}) / (?P<location>[-\w]+). (Décès|Mort) de (?P<name>[-\w]+) (?P<lastName>[-\w]+).'

    @staticmethod
    def extract(text):
        entities = set()
        result = re.finditer(DeathScraper.REGEX, text)
        for g in result:
            p = Person(g.group('name'), g.group('lastName'))
            d = Date.extractDate(g.group('date'))

            if d is None:
                continue

            l = Location(g.group('location'))

            death = Death(d, l, p)
            entities.add(death)
            logging.info("Crafted object: %s", death)

        return entities


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

    REGEX = DATE_AND_LOC_REGEX + '\s+Rencontre\s+(de|entre)\s+(?P<name1>[-\w]+)\s+(?P<lastName1>[-\w]+)\s+(et|avec)\s+(?P<name2>[-\w]+)\s+(?P<lastName2>[-\w]+)'

    @staticmethod
    def extract(text):
        entities = set()
        result = re.finditer(EncounterScraper.REGEX, text)
        for g in result:
            p1 = Person(g.group('name1'), g.group('lastName1'))
            p2 = Person(g.group('name2'), g.group('lastName2'))
            d = Date.extractDate(g.group('date'))

            if d is None:
                continue

            l = Location(g.group('location'))

            e = Encounter(d, l, p1, p2)
            entities.add(e)
            logging.info("Crafted object: %s", e)

        return entities


class ElectionScraper(Scraper):
    """
    A Scapper class psecialized in scrapping elections of individuals
    """

    REGEX = r'(?P<date>[0-9]{4}.[0-9]{2}.[0-9]{2}) / (?P<location>[-\w]+). Election de (?P<name>[-\w]+) (?P<lastName>[-\w]+).'

    @staticmethod
    def extract(text):
        entities = set()
        result = re.finditer(ElectionScraper.REGEX, text)
        for g in result:
            p = Person(g.group('name'), g.group('lastName'))
            d = Date.extractDate(g.group('date'))

            if d is None:
                continue

            l = Location(g.group('location'))

            e = Election(d, l, p)
            entities.add(e)
            logging.info("Crafted object: %s", e)

        return entities


class MariageScraper(Scraper):
    """
    A Scapper class specialized in scrapping mariage of individuals
    """

    REGEX = DATE_AND_LOC_REGEX + '\s+Mariage\s+(de|d\')\s*(?P<name1>[-\w]+)\s+(?P<lastName1>[-\w]+)\s+(avec|et|et d\')\s*(?P<name2>[-\w]+)\s+(?P<lastName2>[-\w]+)'

    @staticmethod
    def extract(text):
        entities = set()
        result = re.finditer(MariageScraper.REGEX, text)
        for g in result:
            p1 = Person(g.group('name1'), g.group('lastName1'))
            p2 = Person(g.group('name2'), g.group('lastName2'))
            d = Date.extractDate(g.group('date'))

            if d is None:
                continue

            l = Location(g.group('location'))

            w = Wedding(d, l, p1, p2)
            entities.add(w)
            logging.info("Crafted object: %s", w)

        return entities


class ParentScraper(Scraper):
    """
    A Scapper class specialized in scrapping parent-child relationships
    """
    REGEX = r'((?P<male>Le père de)|(?P<female>La mère de)) (?P<childName>[-\w]+) (?P<childLastName>[-\w]+) est (?P<parentName>[-\w]+) (?P<parentLastName>[-\w]+).'

    @staticmethod
    def extract(text):
        entities = set()
        result = re.finditer(ParentScraper.REGEX, text)
        for g in result:
            parentName = g.group('parentName')
            parentLastName = g.group('parentLastName')
            childName = g.group('childName')
            childLastName = g.group('childLastName')
            male = g.group('male')
            female = g.group('female')

            sex = ''
            if male is not None:
                sex = 'M'
            elif female is not None:
                sex = 'F'

            parent = Person(parentName, parentLastName, sex)
            child = Person(childName, childLastName)
            parentRelation = Parent(parent, child)
            entities.add(parentRelation)
            logging.info("Crafted object: %s", parent)

        return entities


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

    for i in range(len(responses)):
        response = responses.__getitem__(i)

        if response is None:
            continue

        pageSource = response.read()
        soup = BeautifulSoup(pageSource, 'lxml')
        soupText = str(soup.text)

        births = BirthScraper.extract(soupText)
        deaths = DeathScraper.extract(soupText)
        encounters = EncounterScraper.extract(soupText)
        positions = scrap_generic(soup, PositionScraper)
        elections = ElectionScraper.extract(soupText)
        mariages = MariageScraper.extract(soupText)
        parents = ParentScraper.extract(soupText)

        wikiPage = WikiPage(urlList.__getitem__(i))
        wikiPage.addData(deaths, births, encounters, positions, elections, mariages, parents)
        resData.add(wikiPage)

    return resData


if __name__ == '__main__':
    run(["http://wikipast.epfl.ch/wikipast/index.php/Mariage"])
    run(["http://wikipast.epfl.ch/wikipast/index.php/Rencontre"])
