from Editing.WikiWriter import write_on_page_after_title
from Scraping.WikiInference import BirthInferenceChecker, EncounterInferenceChecker, ElectionInferenceChecker, \
    MariageInferenceChecker


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
    writeOnPages(list_filtered)

def writeOnPages(factsWithPages):
    dict = {}
    for fact in factsWithPages:
        for page in fact[1]:
            value = dict.get(page)
            if value is None:
                dict[page] = [fact[0]]
            else:
                value.append(fact[0])
    for k, e in dict.items():
        head, *tail = e

        head = '* ' + head
        tail = [head] + tail

        s = '\n* '.join(tail)
        write_on_page_after_title(s, k)
