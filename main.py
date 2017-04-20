from InferenceEngine.ForwardChainingWithVariables import ForwardChainingWithVariables
from InferenceEngine.Knowledge import KnowledgeBase
from InferenceEngine.Predicate import Atom, Predicate
from InferenceEngine.RuleWithVariable import RuleWithVariable
from InferenceEngine.Unificator import Unificator

x = Atom('x', True)
y = Atom('y', True)
z = Atom('z', True)

localisation = Atom('localisation', True)

localisation1 = Atom('localisation1', True)
localisation2 = Atom('localisation2', True)

date = Atom('date', True)
l = Atom('l', True)

a = Atom('a', False)
b = Atom('b', False)
c = Atom('c', False)
paris = Atom('Paris', False)
londres = Atom('Londres', False)
mars = Atom('Mars', False)

unificateur = Unificator()

faits = [
    Predicate([a, b, paris], 'Rencontre'),
    Predicate([a, c, paris], 'Rencontre'),
    Predicate([a, londres], 'est localisé'),
    Predicate([b, paris], 'est localisé'),
    Predicate([c, mars], 'est localisé'),
    Predicate([mars, paris], 'est loin'),
    Predicate([mars, londres], 'est loin')
]

regles = [
    [[Predicate([x, y, localisation], 'Rencontre'), Predicate([x, localisation1], 'est localisé'),
      Predicate([y, localisation2], 'est localisé'), Predicate([localisation1, localisation], 'est loin')],
     Predicate([x, y, localisation, localisation1, localisation2], 'Erreur-Rencontre')],
    [[Predicate([x, y, localisation], 'Rencontre'), Predicate([x, localisation1], 'est localisé'),
      Predicate([y, localisation2], 'est localisé'), Predicate([localisation2, localisation], 'est loin')],
     Predicate([x, y, localisation, localisation1, localisation2], 'Erreur-Rencontre')]
]

faits2 = [
    Predicate([a, b], 'pere'),
    Predicate([b, c], 'pere')
]

regles2 = [
    [[Predicate([x, y], 'pere'), Predicate([y, z], 'pere')], Predicate([x, z], 'grand-pere')]
]

bc = KnowledgeBase(lambda descr: RuleWithVariable(descr[0], descr[1]))
bc.addFacts(faits)
bc.addRules(regles)

filtre = unificateur
moteur = ForwardChainingWithVariables(knowledge=bc, method=filtre)
resultat = moteur.chain()

print(resultat)

"""from unittest import TestCase
from moteur_avec_variables.regle_avec_variables import RegleAvecVariables
from moteur_sans_variables.connaissance import BaseConnaissances
from moteur_avec_variables.filtre import Filtre
from moteur_avec_variables.chainage_avant_avec_variables import ChainageAvantAvecVariables

class TestChainageAvantAvecVariables(TestCase):

    def setUp(self):
        self.faits = [
            ('add', '0', '0', '0', '0'),
            ('add', '100', '100', '0', '0'),
            ('add', '100', '0', '100', '0'),
            ('add', '200', '100', '100', '0'),
            ('add', '200', '0', '200', '0'),
            ('add', '300', '100', '200', '0'),
            ('add', '50', '0', '0', '50'),
            ('add', '150', '100', '0', '50'),
            ('add', '150', '0', '100', '50'),
            ('add', '250', '100', '100', '50'),
            ('add', '250', '0', '200', '50'),
            ('add', '350', '100', '200', '50'),
            ('add', '100', '0', '0', '100'),
            ('add', '200', '100', '0', '100'),
            ('add', '200', '0', '100', '100'),
            ('add', '300', '100', '100', '100'),
            ('add', '300', '0', '200', '100'),
            ('add', '400', '100', '200', '100'),
            # Paul
            ('bas-salaire', 'Paul'),
            ('loyer', 'Paul'),
            ('enfants', 'Paul'),
            ('long-trajet', 'Paul'),
            # Marc
            ('moyen-salaire', 'Marc'),
            ('loyer', 'Marc'),
            ('enfants', 'Marc'),
            ('long-trajet', 'Marc'),
            # Jean
            ('haut-salaire', 'Jean'),
            ('pas-de-loyer', 'Jean'),
            ('pas-d-enfants', 'Jean'),
            ('long-trajet', 'Jean'),
        ]

        self.regles = [
            # Réduction enfants
            [[('pas-d-enfants', '?x')], ('réduc-enfant', '0', '?x')],
            [[('enfants', '?x')], ('réduc-enfant', '100', '?x')],
            # Réduction loyer
            [[('bas-salaire', '?x'), ('loyer', '?x')], ('réduc-loyer', '200', '?x')],
            [[('moyen-salaire', '?x'), ('loyer', '?x')], ('réduc-loyer', '100', '?x')],
            [[('haut-salaire', '?x'), ('loyer', '?x')], ('réduc-loyer', '0', '?x')],
            [[('pas-de-loyer', '?x')], ('réduc-loyer', '0', '?x')],
            # Réduction transport
            [[('petit-trajet', '?x')], ('réduc-trajet', '0', '?x')],
            [[('réduc-enfant', '0', '?x'), ('long-trajet', '?x')], ('réduc-trajet', '100', '?x')],
            [[('réduc-loyer', '0', '?x'), ('long-trajet', '?x')], ('réduc-trajet', '100', '?x')],
            [[('réduc-enfant', '100', '?x'), ('réduc-loyer', '100', '?x'), ('long-trajet', '?x')], ('réduc-trajet', '50', '?x')],
            [[('réduc-enfant', '100', '?x'), ('réduc-loyer', '200', '?x'), ('long-trajet', '?x')], ('réduc-trajet', '0', '?x')],
            # Réduction totale
            [[('réduc-enfant', '?a', '?x'), ('réduc-loyer', '?b', '?x'),
              ('réduc-trajet', '?c', '?x'), ('add', '?res', '?a', '?b', '?c')],
             ('réduc', '?res', '?x')],
        ]

    def test_chainage(self):
        buts = [
            ('réduc', '300', 'Paul'),
            ('réduc', '250', 'Marc'),
            ('réduc', '100', 'Jean')
        ]

        bc = BaseConnaissances(lambda descr: RegleAvecVariables(descr[0], descr[1]))
        bc.ajoute_faits(self.faits)
        bc.ajoute_regles(self.regles)

        filtre = Filtre()
        moteur = ChainageAvantAvecVariables(connaissances=bc, methode=filtre)
        resultat = moteur.chaine()

        for but in buts:
            self.assertTrue(but in resultat)

    def test_instancie_conclusion(self):
        bc = BaseConnaissances(lambda descr: RegleAvecVariables(descr[0], descr[1]))
        bc.ajoute_une_regle(self.regles[0])

        filtre = Filtre()
        moteur = ChainageAvantAvecVariables(connaissances=bc, methode=filtre)

        conclusions = moteur.instancie_conclusion(bc.regles[0],
                                                    [{'?x': 'Dupont'},
                                                     {'?x': 'Dupond'}])
        self.assertEqual(conclusions, [('réduc-enfant', '0', 'Dupont'),
                                       ('réduc-enfant', '0', 'Dupond')])

                                       """
