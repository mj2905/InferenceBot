"""
This file defines a keyword for each type of event that can be scrapped on Wikipast's pages. To each keyword
corresponds a list of irrelevant words for the scrapper that should be discared when parsing the corresponding line.

Example:
    
    1234.56.78 / LocationCity. Rencontre de A avec B.
    
    The relevant pieces of information are the date, A and B. Therefore, for the encounter keyword we discard
    "Rencontre", "de" and "avec"
"""
dateTranslationTable = {ord(c): None for c in '-'}
translationTable = {ord(c): None for c in '0123456789|[](){}.:;/*%&?!^='}

BIRTH = "Naissance"
DEATH = "Mort"

BEFORE = "avant"
AFTER = "apres"

BIRTH_TODISCARD = ["Naissance", "de"]
DEATH_TODISCARD = ["Mort", "de"]


ENCOUNTER = "Rencontre"
ENCOUNTER_TODISCARD = ["Rencontre", "de", "avec", "entre", "et"]

ERROR_DATE = "Erreur de date"
