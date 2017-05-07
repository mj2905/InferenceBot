from InferenceEngine.Predicate import Atom, Predicate

# Date Variables
from Scraping import WikiStrings

d1 = Atom('d1', True)
d2 = Atom('d2', True)
d3 = Atom('d3', True)

# Location Variables
l1 = Atom('l1', True)
l2 = Atom('l2', True)
l3 = Atom('l3', True)

# Person Variables
p1 = Atom('p1', True)
p2 = Atom('p2', True)

# Name of Predicate
before = WikiStrings.BEFORE
after = WikiStrings.AFTER
birth = WikiStrings.BIRTH
death = WikiStrings.DEATH
error_date = WikiStrings.ERROR_DATE
encounter = WikiStrings.ENCOUNTER
position = WikiStrings.POSITION
election = WikiStrings.ELECTION
# close = WikiStrings.CLOSE
far = WikiStrings.FAR
error_encounter = WikiStrings.ERROR_ENCOUNTER

error_election = WikiStrings.ERROR_ELECTION

# Rules
DEATH_BIRTH_RULES = [
    # [[Predicate([y, x], before)], Predicate([x, y], after)],
    #  [[Predicate([y, x], after)], Predicate([x, y], before)],
    [[Predicate([d1, l1, p1], birth), Predicate([d2, l2, p1], death), Predicate([d2, d1], before)],
     Predicate([p1, d1, d2], error_date)]]

# Rules
ENCOUNTER_RULES = [
    [[Predicate([d1, l1, p1, p2], encounter), Predicate([d1, l2, p1], position),
      Predicate([l1, l2], far)],
     Predicate([d1, l1, l2, p1, p2], error_encounter)],
    [[Predicate([d1, l1, p1, p2], encounter), Predicate([d1, l2, p2], position),
      Predicate([l1, l2], far)],
     Predicate([d1, l1, l2, p1, p2], error_encounter)]]

# Rules
ELECTION_RULES = [
    [[Predicate([d1, l1, p1], birth), Predicate([d2, l2, p1], death), Predicate([d3, l3, p1], election),
    Predicate([d3, d2], before), Predicate([d3, d1], before)],
    Predicate([d1, d2, d3, l1, l2, l3, p1], error_election)],
    [[Predicate([d1, l1, p1], birth), Predicate([d2, l2, p1], death), Predicate([d3, l3, p1], election),
    Predicate([d1, d3], before), Predicate([d2, d3], before)],
    Predicate([d1, d2, d3, l1, l2, l3, p1], error_election)],
    [[Predicate([d1, l1, p1], birth), Predicate([d2, l2, p1], death), Predicate([d3, l3, p1], election),
    Predicate([d3, d1], before), Predicate([d2, d3], before)],
    Predicate([d1, d2, d3, l1, l2, l3, p1], error_election)]
]

# Rule ideas:
    #Date de Distinction > Date naissance
    #Date d'Election > Date naissance et < Date mort
    #Naissance enfant > naissance personne en question
    #Hypermot nécessitant un nom mais qui n'est pas suivi d'un nom (naissance sans nom de l'enfant, election, ...)
    #Autres pages intéressantes : Mariage, démission, nomination, participation
