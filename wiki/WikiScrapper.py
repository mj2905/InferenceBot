import urllib.request as urllib

from bs4 import BeautifulSoup

from Datastructs import *

baseUrl = 'http://wikipast.epfl.ch/wikipast/index.php/'
listPage = 'InferenceBot_-_Listes_des_pages_de_test'


def run():
    people = []

    response = urllib.urlopen(baseUrl + listPage)
    pageSource = response.read()
    soup = BeautifulSoup(pageSource, 'html.parser')

    listDiv = soup.find(text="Liste des personnes").parent.parent

    # What if the list is empty ?
    li = listDiv.findNext("li")

    while (li != None):
        p = li.findNext("a").text
        p = p[p.find('-') + 2:]
        (name, lastName) = p.split(" ")
        people.append(Person(name, lastName))
        li = li.find_next_sibling("li")


if __name__ == '__main__':
    run()
