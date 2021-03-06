"""
This file defines a keyword for each type of event that can be scrapped on Wikipast's pages. To each keyword
corresponds a list of irrelevant words for the scrapper that should be discared when parsing the corresponding line.

Example:

    1234.56.78 / LocationCity. Rencontre de A avec B.

    The relevant pieces of information are the date, A and B. Therefore, for the encounter keyword we discard
    "Rencontre", "de" and "avec"
"""
dateTranslationTable = {ord(c): None for c in '-"aàäöüéè\'bcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ: *'}
translationTable = {ord(c): None for c in '0123456789|[](){}.,:;/*%&?!^='}

BIRTH = "Naissance"
DEATH = "Mort"

BEFORE = "avant"
AFTER = "apres"
DIFFERENT = "different"
SAME = "same"

BIRTH_TODISCARD = 'Naissance de '
DEATH_TODISCARD = 'Mort de '
POSITION_TODISCARD = '\w+ de '

CLOSE = "proche"
FAR = "loin"

DATE_AND_LOC_REGEX = '(?P<date>[0-9]{4}\.*[0-9]{0,2}\.*[0-9]{0,2})\s*/\s*(?P<location>[-\w]*)\.*'

ENCOUNTER = "Rencontre"
ENCOUNTER_TODISCARD = ["Rencontre", "de", "avec", "entre", "et"]

ELECTION = "Election"
ELECTION_TODISCARD = 'Election de '

MARIAGE = "Mariage"
MARIAGE_TODISCARD = ["Mariage", "de", "avec", "entre", "et"]

DIVORCE = "Divorce"

POSITION = "Position"

FATHER = "père"
GRANDFATHER = "grand-père"
SON = "fils"

ERROR_DATE = "Erreur de date"
ERROR_BIRTH = "Plusieurs naissances"
ERROR_DEATH = "Plusieurs morts"
WARNING_ENCOUNTER = "Attention, erreur potentielle de rencontre"
ERROR_ELECTION = "Erreur d'election"
ERROR_MARIAGE = "Erreur de mariage"
DIVORCE_INFERENCE = "Divorce possible"

def validWikiUrl(url):
    if url in ["#", None]:
        return False
    if -1 != url.find("Wikipast:"):
        return False
    return True
