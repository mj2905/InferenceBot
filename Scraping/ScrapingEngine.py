import logging
import re
import time
import urllib.request as urllib
import urllib.parse as urlparse

import requests
from bs4 import BeautifulSoup

import Scraping.WikiScraper
from DataStructures.Datastructs import WikiData
from Scraping.WikiStrings import validWikiUrl

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.ERROR)

discussionTag = "Discussion:"
fichierTag = "Fichier:"

class ScrapingEngine(object):
    def __init__(self):
        self.linksDB = set()
        self.objectsDB = WikiData()
        self.baseUrl = 'http://wikipast.epfl.ch'
        self.urlTitlePrefix = self.baseUrl + '/wikipast/index.php/'
        self.listPage = '/wikipast/index.php/Sp%C3%A9cial:Toutes_les_pages'

    def buildLinkDatabase(self, data, dateBegin, limit=-1):
        logging.info("Building link database. Considering modifications since " + dateBegin)
        baseurl = 'http://wikipast.epfl.ch/wikipast/'

        protected_logins = ["Frederickaplan", "Maud", "Vbuntinx", "InferenceBot", "Testbot", "IB", "SourceBot", "PageUpdaterBot",
                            "Orthobot", "BioPathBot", "ChronoBOT", "Amonbaro", "AntoineL", "AntoniasBanderos", "Arnau",
                            "Arnaudpannatier", "Aureliver", "Brunowicht", "Burgerpop", "Cedricviaccoz", "Christophe",
                            "Claudioloureiro", "Ghislain", "Gregoire3245", "Hirtg", "Houssm", "Icebaker", "JenniCin",
                            "JiggyQ", "JulienB", "Kl", "Kperrard", "Leandro Kieliger", "Marcus", "Martin",
                            "MatteoGiorla",
                            "Mireille", "Mj2905", "Musluoglucem", "Nacho", "Nameless", "Nawel", "O'showa", "PA",
                            "Qantik",
                            "QuentinB", "Raphael.barman", "Roblan11", "Romain Fournier", "Sbaaa", "Snus", "Sonia",
                            "Tboyer",
                            "Thierry", "Titi", "Vlaedr", "Wanda"]

        for user in protected_logins:
            result = requests.post(
                baseurl + 'api.php?action=query&list=usercontribs&ucuser=' + user + '&format=xml&uclimit=500&ucdir=newer&ucstart=' + dateBegin)
            soup = BeautifulSoup(result.content, 'lxml')

            for primitive in soup.usercontribs.findAll('item'):
                if discussionTag not in primitive['title'] and fichierTag not in primitive['title']:
                    page = urlparse.quote_plus(str(re.sub('\s+', '_', str(primitive['title']))))
                    self.linksDB.add(''.join([self.urlTitlePrefix, page]))

        for link in self.linksDB:
            logging.info("%s", link)

        # Validate links
        self.linksDB = set([x for x in self.linksDB if validWikiUrl(x)])

    def processUrlBatch(self, batch):
        logging.info("Attempting to scrape: %s", batch)
        results = Scraping.WikiScraper.run(batch)
        self.objectsDB.joinWith(results)

    def run(self, dateBegin, batchSize=10):
        start = time.time()
        response = urllib.urlopen(self.baseUrl + self.listPage)

        pageSource = response.read()
        soup = BeautifulSoup(pageSource, 'lxml')

        self.buildLinkDatabase(soup, dateBegin)

        urlBatch = list()
        i = 0
        for l in self.linksDB:
            if "ImageBot" in l:
                print("got")

            urlBatch.append(l)
            i += 1

            if (i >= batchSize):
                self.processUrlBatch(urlBatch)
                urlBatch.clear()
                i = 0
        self.processUrlBatch(urlBatch)

        end = time.time()
        logging.info("%s", str(self.objectsDB))
        logging.info("Processing time was %f second(s).", end - start)

    def getResultSet(self):
        return self.objectsDB

    def isReady(self):
        return len(self.linksDB) != 0

    def clear(self):
        self.clearLinks()
        self.clearResults()

    def clearLinks(self):
        self.linksDB = set()

    def clearResults(self):
        self.objectsDB.clear()

if __name__ == '__main__':
    scEng = ScrapingEngine()
    scEng.run()
