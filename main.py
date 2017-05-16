from Editing.WikiWriter import *
from Scraping.WikiInference import *
from Scraping.WikiStrings import *


def write_inferences(resData):

    birth_facts = BirthInferenceChecker()
    encounter_facts = EncounterInferenceChecker()
    election_facts = ElectionInferenceChecker()
    mariage_facts = MariageInferenceChecker()


    list_birth_facts = birth_facts.checkIfErrors(resData)
    list_encounter_facts = encounter_facts.checkIfErrors(resData)
    list_election_facts = election_facts.checkIfErrors(resData)
    list_mariage_facts = mariage_facts.checkIfErrors(resData)

    list_facts = []
    if list_birth_facts is not None:
        list_facts.extend(list_birth_facts)
    if list_encounter_facts is not None:
        list_facts.extend(list_encounter_facts)
    if list_election_facts is not None:
        list_facts.extend(list_election_facts)
        #  if list_mariage_facts is not None:
        #     list_facts.extend(list_mariage_facts)

    list_filtered = pretty(list_facts)

    head, *tail = list_filtered

    head = '* ' + head
    tail = [head] + tail

    s = '\n* '.join(tail)
    write_on_page(s)


def pretty(list_facts):
    list_pretty = []
    for elem in list_facts:
        if ERROR_DATE in elem.name:
            list_pretty.append(elem.name + " : [[" + elem.propositions[0].name + "]] né en " + elem.propositions[1].name
                + " et mort en " + elem.propositions[2].name)
        elif WARNING_ENCOUNTER in elem.name:
            list_pretty.append(elem.name + " : [[" + elem.propositions[3].name + "]] et [[" + elem.propositions[4].name
                + "]] se sont rencontrés à [[" + elem.propositions[1].name + "]] et à [[" + elem.propositions[2].name
                + "]] en même temps à la date " + elem.propositions[0].name)
        elif ERROR_BIRTH in elem.name:
            list_pretty.append(elem.name + " : [[" + elem.propositions[0].name + "]] né en " + elem.propositions[1].name
                + " et né en " + elem.propositions[2].name)
        elif ERROR_DEATH in elem.name:
            list_pretty.append(elem.name + " : [[" + elem.propositions[0].name + "]] mort en "
                + elem.propositions[1].name + " et mort en " + elem.propositions[2].name)
        elif ERROR_ELECTION in elem.name:
            list_pretty.append(elem.name + " : [[" + elem.propositions[6].name + "]] (" + elem.propositions[0].name
                + " / " + elem.propositions[1].name + ")"+ " est élu en " + elem.propositions[2].name + " à [[" + elem.propositions[5].name + "]]")
        elif ERROR_MARIAGE in elem.name:
            list_pretty.append(elem.name + " : [[" + elem.propositions[6].name + " ]] (" + elem.propositions[0].name
                + " / " + elem.propositions[1].name + ") et " + elem.propositions[7].name + " se marient le "
                + elem.propositions[2].name + " à [[" + elem.propositions[5].name + "]]")
    return list_pretty

def main():
    write_inferences()

if __name__ == '__main__':
    main()
