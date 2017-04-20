from ForwardChainingWithVariables import ForwardChainingWithVariables
from Knowledge import KnowledgeBase
from Predicate import Atom, Predicate
from RuleWithVariable import RuleWithVariable
from Unificator import Unificator

x = Atom('x',True)
y = Atom('y',True)
z = Atom('z',True)


a = Atom('a',False)
b = Atom('b',False)
c = Atom('c',False)
unificateur = Unificator()

faits = [
    Predicate([a,b],'pere'),
    Predicate([b,c],'pere')
]

regles = [
    [[Predicate([x,y], 'pere'),Predicate([y,z], 'pere')],Predicate([x,z],'grand-pere')]
]

bc = KnowledgeBase(lambda descr: RuleWithVariable(descr[0], descr[1]))
bc.addFacts(faits)
bc.addRules(regles)

filtre = unificateur
moteur = ForwardChainingWithVariables(knowledge=bc, method=filtre)
resultat = moteur.chain()

print(resultat)