import re

"""

# Nom de variables
x = Atom('x', True)
y = Atom('y', True)
z = Atom('z', True)
k = Atom('k', True)
l = Atom('l', True)

localisation = Atom('localisation', True)
localisation1 = Atom('localisation1', True)
localisation2 = Atom('localisation2', True)

# Nom des constantes
a = Atom('a', False)
b = Atom('b', False)
c = Atom('c', False)

paris = Atom('Paris', False)
londres = Atom('Londres', False)
mars = Atom('Mars', False)

date1 = Atom('date1', False)
date2 = Atom('date2', False)
date3 = Atom('date3', False)

unificateur = Unificator()

# Exemple 1
faits1 = [
    Predicate([a, b, paris], 'Rencontre'),
    Predicate([a, c, paris], 'Rencontre'),
    Predicate([a, londres], 'est localisé'),
    Predicate([b, paris], 'est localisé'),
    Predicate([c, mars], 'est localisé'),
    Predicate([mars, paris], 'est loin'),
    Predicate([mars, londres], 'est loin')
]

regles1 = [
    [[Predicate([x, y, localisation], 'Rencontre'), Predicate([x, localisation1], 'est localisé'),
      Predicate([y, localisation2], 'est localisé'), Predicate([localisation1, localisation], 'est loin')],
     Predicate([x, y, localisation, localisation1, localisation2], 'Erreur-Rencontre')],
    [[Predicate([x, y, localisation], 'Rencontre'), Predicate([x, localisation1], 'est localisé'),
      Predicate([y, localisation2], 'est localisé'), Predicate([localisation2, localisation], 'est loin')],
     Predicate([x, y, localisation, localisation1, localisation2], 'Erreur-Rencontre')]
]

#Exemple 2
faits2 = [
    Predicate([a, b], 'pere'),
    Predicate([b, c], 'pere')
]

regles2 = [
    [[Predicate([x, y], 'pere'), Predicate([y, z], 'pere')], Predicate([x, z], 'grand-pere')]
]

# Exemple 3
faits3 = [
    Predicate([a, date1], 'né'),
    Predicate([b, date2], 'né'),
    Predicate([a, date3], 'mort'),
    Predicate([b, date3], 'mort'),
    Predicate([date1, date3], 'avant'),
    Predicate([date2, date3], 'apres'),
    Predicate([date1, date2], 'avant')
]

regles3 = [
    [[Predicate([y, x], 'avant')], Predicate([x, y], 'apres')],
    [[Predicate([y, x], 'apres')], Predicate([x, y], 'avant')],
    [[Predicate([x, y], 'né'), Predicate([x, k], 'mort'), Predicate([y, k], 'apres')],
     Predicate([x, y, k], 'Error-Date')]
]

bc = KnowledgeBase(lambda descr: RuleWithVariable(descr[0], descr[1]))

# Vous pouvez essayer les différents exemples pour regarder ce que ca donne. :-)
bc.addFacts(faits3)
bc.addRules(regles3)

filtre = unificateur
moteur = ForwardChainingWithVariables(knowledge=bc, method=filtre)
resultat = moteur.chain()

print(type(resultat))


"""

s = '1234.12.12 / Rome. Naissance de Secundinus Aurelianus.'
print(re.sub('\w+ de ', '', s))
