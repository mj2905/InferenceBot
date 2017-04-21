import logging
import time
import urllib.request as urllib

from bs4 import BeautifulSoup

import Scraping.WikiScraper

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)


class ScrapingEngine(object):
    def __init__(self):
        self.linksDB = set()
        self.objectsDB = set()
        self.baseUrl = 'http://wikipast.epfl.ch'
        self.listPage = '/wikipast/index.php/Sp%C3%A9cial:Toutes_les_pages'

    def buildLinkDatabase(self, data, limit=-1):
        logging.info("Building link database")
        i = 0
        for link in data.find_all('a'):
            if (limit != -1 and i > limit):
                break;
            else:
                logging.debug("Added link to database: %s", link.get("href"))
                self.linksDB.add(link.get("href"))
                i += 1

        # Validate links
        self.linksDB = [x for x in self.linksDB if x not in ["#", None]]

    def processUrlBatch(self, batch):
        # logging.info("Attempting to scrape: %s", batch)
        results = Scraping.WikiScraper.run(batch)
        # logging.info("%s was scraped resulting in %s", batch, results)

    def run(self, batchSize=10):
        start = time.time()
        response = urllib.urlopen(self.baseUrl + self.listPage)

        pageSource = response.read()
        soup = BeautifulSoup(pageSource, 'lxml')

        self.buildLinkDatabase(soup, 100)

        urlBatch = list()
        i = 0
        for l in self.linksDB:
            urlBatch.append(''.join([self.baseUrl, l]))
            i += 1

            if (i >= batchSize):
                self.processUrlBatch(urlBatch)
                urlBatch.clear()
                i = 0
        self.processUrlBatch(urlBatch)

        end = time.time()

        logging.info("Processing time was %f second(s).", end - start)


if __name__ == '__main__':
    scEng = ScrapingEngine()
    scEng.run()
