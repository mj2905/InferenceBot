from Scraping.WikiInference import BirthInferenceChecker, EncounterInferenceChecker
from Editing.WikiWriter import *

def write_birth_check():

    toKeep = 'Erreur'

    bic = BirthInferenceChecker()
    eic = EncounterInferenceChecker()
    listBic = bic.checkIfErrors()
    listEic = eic.checkIfErrors()
    
    list = []
    if listBic is not None:
        list.extend(listBic)
    if listEic is not None:
        list.extend(listEic)
    

    listFiltered = pretty(list)

    head, *tail = listFiltered

    head = '* ' + head
    tail = [head] + tail

    s = '\n* '.join(tail)
    write_on_page(s)


def pretty(list):
    newList = []
    for elem in list:
        if("Erreur de date" in elem.name):
            newList.append(elem.name + " : [[" + elem.propositions[0].name + "]] né en " + elem.propositions[1].name + " et mort en " + elem.propositions[2].name)
        elif("Erreur de rencontre" in elem.name):
            newList.append(elem.name + " : [[" + elem.propositions[3].name + "]] et [[" + elem.propositions[4].name + "]] se sont rencontrés à [[" + elem.propositions[1].name + "]] et à [[" + elem.propositions[2].name + "]] en même temps à la date " + elem.propositions[0].name)
    return newList

write_birth_check()
