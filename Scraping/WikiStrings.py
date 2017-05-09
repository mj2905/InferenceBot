"""
This file defines a keyword for each type of event that can be scrapped on Wikipast's pages. To each keyword
corresponds a list of irrelevant words for the scrapper that should be discared when parsing the corresponding line.

Example:

    1234.56.78 / LocationCity. Rencontre de A avec B.

    The relevant pieces of information are the date, A and B. Therefore, for the encounter keyword we discard
    "Rencontre", "de" and "avec"
"""
dateTranslationTable = {ord(c): None for c in '-'}
translationTable = {ord(c): None for c in '0123456789|[](){}.,:;/*%&?!^='}


BEFORE = "avant"
AFTER = "apres"
DIFFERENT = "different"
SAME = "same"

BIRTH = "Naissance"
BIRTH_TODISCARD = 'Naissance de '

DEATH = "Décès"
DEATH_TODISCARD = ["Mort", "Décès", "de"]
POSITION_TODISCARD = '\w+ de '

CLOSE = "proche"
FAR = "loin"


ENCOUNTER = "Rencontre"
ENCOUNTER_TODISCARD = ["Rencontre", "de", "avec", "entre", "et"]

ELECTION = "Election"
ELECTION_TODISCARD = 'Election de '

POSITION = "Position"

ERROR_DATE = "Erreur de date"
ERROR_BIRTH = "Plusieurs naissances"
ERROR_DEATH = "Plusieurs morts"
WARNING_ENCOUNTER = "Attention, erreur potentielle de rencontre"
ERROR_ELECTION = "Erreur d'election"


def validWikiUrl(url):
    if url in ["#", None]:
        return False
    if url.startswith("http") or url.startswith("www") or url.startswith("/www"):
        return False
    if -1 != url.find("Wikipast:"):
        return False
    return True
