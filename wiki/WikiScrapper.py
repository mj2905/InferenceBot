import logging
import urllib.request as urllib

from bs4 import BeautifulSoup

from Datastructs import *
from wiki import WikiStrings

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

baseUrl = 'http://wikipast.epfl.ch/wikipast/index.php/'
listPage = 'InferenceBot_page_test_-_Secundinus_Aurelianus'


def scrap_encounters(data):
    """
    Function for scrapping all encounters from a Wikipast page. It does not rely on a particular page layout.
    Instead, it looks for occurrences of the encounter keyword (as defined in the WikiStrings file) and extracts 
    encounter data from the corresponding lines.
    
    The usual encounter format is the following:
    
    1234.56.78 / LocationCity. Rencontre de A avec B.
    
    The line is first split at '/' to retrieve the date, then at the first point to retrieve the location and
    finally splits the remaining string at each space. The resulting list is filtered according to the list of 
    words to discard as given in the WikiStrings file and the Encounter object is creating with the remaining data.
    This data is assumed to be the first and last name of both protagonists, nothing more, nothing less. If the 
    remaining data does not math the format expected it is discarded and the entry is logged.
    
    :param data: The source code of the page as given by BeautifulSoup's parser
    :return: A set containing all encounters that have been recognized. Unrecognizable ones are logged.
    """
    scrappedEncounters = set()
    encounters = data.findAll(string=WikiStrings.ENCOUNTER)

    logging.info("The scrapper found %d candidate entries for encounters", len(encounters))
    for encounter in encounters:
        tag = encounter.parent.parent
        candidateStr = tag.text
        logging.debug("Candidate for encounter is %s", candidateStr)

        (date, locAndPeople) = candidateStr.split("/")
        (location, people) = locAndPeople.split(".", 1)  # Specify at most 1 split to retrieve location

        # Extract only people's names
        people = people.strip().split(" ")
        people = [x for x in people if x not in WikiStrings.ENCOUNTER_TODISCARD]

        if (len(people) != 4):
            logging.warning("The scrapper discarded a candidate encounter because it " +
                            "did not have the correct number of names in it. " +
                            "The discarded entry is %s", candidateStr)
            continue

        p1 = Person(people[0], people[1])
        p2 = Person(people[2], people[3])
        d = Date.extractDate(date)
        e = Encounter(d, p1, p2)

        logging.info("Crafted Encounter object: %s", str(e))
        scrappedEncounters.add(e)

    return scrappedEncounters


def scrapBirth():
    pass

def run():
    people = []

    response = urllib.urlopen(baseUrl + listPage)
    pageSource = response.read()
    soup = BeautifulSoup(pageSource, 'lxml')
    scrap_encounters(soup)

if __name__ == '__main__':
    run()
