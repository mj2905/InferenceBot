from abc import ABCMeta, abstractmethod

from InferenceEngine.ForwardChainingWithVariables import ForwardChainingWithVariables
from InferenceEngine.Knowledge import KnowledgeBase
from InferenceEngine.RuleWithVariable import RuleWithVariable
from InferenceEngine.Unificator import Unificator
from Scraping import WikiRules
from Scraping import WikiScraper


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
        super().__init__(WikiRules.DEATH_BIRTH_RULES, facts)

    def checkIfErrors(self):

        # Insert the url to check from
        births, deaths = \
        WikiScraper.run(['http://wikipast.epfl.ch/wikipast/index.php/InferenceBot_page_test_-_Secundinus_Aurelianus'])[
            0]

        birthsFacts = list(map(lambda x: x.toPredicate(), births))
        deathFacts = list(map(lambda x: x.toPredicate(), deaths))

        self.addFacts(birthsFacts)
        self.addFacts(deathFacts)

        for d in deaths:
            for b in births:
                self.addFact(d.date.isBeforePredicate(b.date))

        return self.moteur.chain()


if __name__ == '__main__':
    t = BirthInferenceChecker()
    print(t.checkIfErrors())
