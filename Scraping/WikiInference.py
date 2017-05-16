from abc import ABCMeta, abstractmethod

from InferenceEngine.ForwardChainingWithVariables import ForwardChainingWithVariables
from InferenceEngine.Knowledge import KnowledgeBase
from InferenceEngine.RuleWithVariable import RuleWithVariable
from InferenceEngine.Unificator import Unificator
from Scraping import WikiRules
from Scraping.WikiRules import B_RULES


class InferenceChecker(metaclass=ABCMeta):
    def __init__(self, rules, facts=None):
        if facts is None:
            facts = []
        self.rules = rules

        self.bc = KnowledgeBase(lambda descr: RuleWithVariable(descr[0], descr[1]))
        self.bc.addFacts(facts)
        self.bc.addRules(rules)
        unificator = Unificator()
        self.moteur = ForwardChainingWithVariables(knowledge=self.bc, method=unificator)

    def addFact(self, fact):
        self.bc.addFact(fact)

    def addFacts(self, facts):
        self.bc.addFacts(facts)

    @abstractmethod
    def checkIfErrors(self):
        pass


class BirthInferenceChecker(InferenceChecker):
    def __init__(self, facts=None):
        super().__init__(B_RULES, facts)

    def checkIfErrors(self, resData):

        # Insert the url to check from
        #resData =
            #WikiScraper.run(
             #   ['http://wikipast.epfl.ch/wikipast/index.php/InferenceBot_page_test_-_Secundinus_Aurelianus',
             #   'http://wikipast.epfl.ch/wikipast/index.php/InferenceBot_page_test_-_Laurentinus_Porcius'])

        birthsFacts = []
        deathFacts = []

        births = []
        deaths = []

        for page in resData.data:

            birthsWithoutNone = list(filter(lambda x: x is not None,page.births))
            deathsWithoutNone = list(filter(lambda x: x is not None,page.deaths))

            birthsFacts.extend(list(map(lambda x: x.toPredicate(page.url), birthsWithoutNone)))
            births.extend(birthsWithoutNone)
            deathFacts.extend(list(map(lambda x: x.toPredicate(page.url), deathsWithoutNone)))
            deaths.extend(deathsWithoutNone)

        self.addFacts(birthsFacts)
        self.addFacts(deathFacts)

        for d in deaths:
            for b in births:
                self.addFact(d.date.isBeforePredicate(b.date))

        for i in range(0, len(births)):
            for j in range(i, len(births)):
                self.addFact(births[i].date.isDifferentPredicate(births[j].date))

        for i in range(0, len(deaths)):
            for j in range(i, len(deaths)):
                self.addFact(deaths[i].date.isDifferentPredicate(deaths[j].date))

        return self.moteur.chain()


class EncounterInferenceChecker(InferenceChecker):
    def __init__(self, facts=None):
        super().__init__(WikiRules.ENCOUNTER_RULES, facts)

    def checkIfErrors(self, resData):

        # Insert the url to check from
        #resData = \
        #    WikiScraper.run(
        #        ['http://wikipast.epfl.ch/wikipast/index.php/InferenceBot_page_test_-_Secundinus_Aurelianus',
        #         'http://wikipast.epfl.ch/wikipast/index.php/InferenceBot_page_test_-_Pompilius_Iuvenalis',
        #         'http://wikipast.epfl.ch/wikipast/index.php/InferenceBot_page_test_-_Varius_Maxentius'])

        encountersFacts = []
        positionsFacts = []

        encounters = []
        positions = []

        for page in resData.data:

            encountersWithoutNone = list(filter(lambda x: x is not None,page.encounters))
            positionsWithoutNone = list(filter(lambda x: x is not None,page.positions))

            encountersFacts.extend(list(map(lambda x: x.toPredicate(page.url), encountersWithoutNone)))
            encounters.extend(encountersWithoutNone)
            positionsFacts.extend(list(map(lambda x: x.toPredicate(page.url), positionsWithoutNone)))
            positions.extend(positionsWithoutNone)

        self.addFacts(encountersFacts)
        self.addFacts(positionsFacts)

        for e in encounters:
            for p in positions:
                temp = e.location.isFarPredicate(p.location)
                if temp is not None:
                    if e.person1 == p.person:
                        self.addFact(temp)
                    if e.person2 == p.person:
                        self.addFact(temp)

        return self.moteur.chain()


class ElectionInferenceChecker(InferenceChecker):
    def __init__(self, facts=None):
        super().__init__(WikiRules.ELECTION_RULES, facts)

    def checkIfErrors(self, resData):

        #resData = \
        #    WikiScraper.run(
        #        ['http://wikipast.epfl.ch/wikipast/index.php/InferenceBot_page_test_-_Secundinus_Aurelianus'])

        electionsFacts = []
        birthsFacts = []
        deathFacts = []

        elections = []
        births = []
        deaths = []

        for page in resData.data:

            electionsWithoutNone = list(filter(lambda x: x is not None,page.elections))
            birthsWithoutNone = list(filter(lambda x: x is not None,page.births))
            deathsWithoutNone = list(filter(lambda x: x is not None, page.deaths))

            electionsFacts.extend(list(map(lambda x: x.toPredicate(page.url), electionsWithoutNone)))
            elections.extend(electionsWithoutNone)
            birthsFacts.extend(list(map(lambda x: x.toPredicate(page.url), birthsWithoutNone)))
            births.extend(birthsWithoutNone)
            deathFacts.extend(list(map(lambda x: x.toPredicate(page.url), deathsWithoutNone)))
            deaths.extend(deathsWithoutNone)

        self.addFacts(electionsFacts)
        self.addFacts(birthsFacts)
        self.addFacts(deathFacts)

        for e in elections:
            for d in deaths:
                self.addFact(d.date.isBeforePredicate(e.date))
            for b in births:
                self.addFact(e.date.isBeforePredicate(b.date))

        return self.moteur.chain()

class MariageInferenceChecker(InferenceChecker):
    def __init__(self, facts=None):
        super().__init__(WikiRules.MARIAGE_RULES, facts)

    def checkIfErrors(self, resData):

        #resData = \
        #    WikiScraper.run(
        #        ['http://wikipast.epfl.ch/wikipast/index.php/InferenceBot_page_test_-_Secundinus_Aurelianus',
        #        'http://wikipast.epfl.ch/wikipast/index.php/InferenceBot_page_test_-_Laurentinus_Porcius'])

        mariagesFacts = []
        birthsFacts = []
        deathFacts = []

        mariages = []
        births = []
        deaths = []

        for page in resData.data:

            weddingsWithoutNone = list(filter(lambda x: x is not None,page.weddings))
            birthsWithoutNone = list(filter(lambda x: x is not None,page.births))
            deathsWithoutNone = list(filter(lambda x: x is not None, page.deaths))

            mariagesFacts.extend(list(map(lambda x: x.toPredicate(page.url), weddingsWithoutNone)))
            mariages.extend(weddingsWithoutNone)
            birthsFacts.extend(list(map(lambda x: x.toPredicate(page.url), birthsWithoutNone)))
            births.extend(birthsWithoutNone)
            deathFacts.extend(list(map(lambda x: x.toPredicate(page.url), deathsWithoutNone)))
            deaths.extend(deathsWithoutNone)

        self.addFacts(mariagesFacts)
        self.addFacts(birthsFacts)
        self.addFacts(deathFacts)


        for m in mariages:
            for d in deaths:
                if m.person1 == d.person or m.person2 == d.person :
                    self.addFact(d.date.isBeforePredicate(m.date))
            for b in births:
                if m.person1 == b.person or m.person2 == b.person :
                    self.addFact(m.date.isBeforePredicate(b.date))

        return self.moteur.chain()

class DivorceInferenceChecker(InferenceChecker):
    def __init__(self, facts=None):
        super().__init__(WikiRules.DIVORCE_RULES, facts)

    def checkIfErrors(self, resData):

        #resData = \
        #    WikiScraper.run(
        #        ['http://wikipast.epfl.ch/wikipast/index.php/InferenceBot_page_test_-_Secundinus_Aurelianus',
        #        'http://wikipast.epfl.ch/wikipast/index.php/InferenceBot_page_test_-_Laurentinus_Porcius'])

        mariagesFacts = []
        birthsFacts = []
        deathFacts = []

        mariages = []
        births = []
        deaths = []

        for page in resData.data:
            weddingsWithoutNone = list(filter(lambda x: x is not None, page.weddings))
            birthsWithoutNone = list(filter(lambda x: x is not None, page.births))
            deathsWithoutNone = list(filter(lambda x: x is not None, page.deaths))

            mariagesFacts.extend(list(map(lambda x: x.toPredicate(page.url), weddingsWithoutNone)))
            mariages.extend(weddingsWithoutNone)
            birthsFacts.extend(list(map(lambda x: x.toPredicate(page.url), birthsWithoutNone)))
            births.extend(birthsWithoutNone)
            deathFacts.extend(list(map(lambda x: x.toPredicate(page.url), deathsWithoutNone)))
            deaths.extend(deathsWithoutNone)

        self.addFacts(mariagesFacts)
        self.addFacts(birthsFacts)
        self.addFacts(deathFacts)


        for m in mariages:
            for d in deaths:
                if m.person1 == d.person or m.person2 == d.person :
                    self.addFact(d.date.isBeforePredicate(m.date))
            for b in births:
                if m.person1 == b.person or m.person2 == b.person :
                    self.addFact(m.date.isBeforePredicate(b.date))

        return self.moteur.chain()

if __name__ == '__main__':
    pass
    #t = EncounterInferenceChecker()
    #print(t.checkIfErrors())
