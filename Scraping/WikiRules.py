from InferenceEngine.Predicate import Atom, Predicate

# Date Variables
from Scraping import WikiStrings

d1 = Atom('d1', True)
d2 = Atom('d2', True)
d3 = Atom('d3', True)
d4 = Atom('d4', True)
d5 = Atom('d5', True)

# Location Variables
l1 = Atom('l1', True)
l2 = Atom('l2', True)
l3 = Atom('l3', True)
l4 = Atom('l4', True)
l5 = Atom('l5', True)

# Person Variables
p1 = Atom('p1', True)
p2 = Atom('p2', True)
p3 = Atom('p3', True)

# Name of Predicate
before = WikiStrings.BEFORE
different = WikiStrings.DIFFERENT
#  after = WikiStrings.AFTER
after = WikiStrings.AFTER
birth = WikiStrings.BIRTH
death = WikiStrings.DEATH
error_date = WikiStrings.ERROR_DATE
encounter = WikiStrings.ENCOUNTER
position = WikiStrings.POSITION
election = WikiStrings.ELECTION
mariage = WikiStrings.MARIAGE
divorce = WikiStrings.DIVORCE_INFERENCE
# close = WikiStrings.CLOSE
far = WikiStrings.FAR
error_multi_birth = WikiStrings.ERROR_BIRTH
error_multi_death = WikiStrings.ERROR_DEATH
warning_encounter = WikiStrings.WARNING_ENCOUNTER

father = WikiStrings.FATHER
grandfather = WikiStrings.GRANDFATHER
son = WikiStrings.SON

error_election = WikiStrings.ERROR_ELECTION
error_mariage = WikiStrings.ERROR_MARIAGE
# Rules

BIRTH_MULTITIMES = [[[Predicate([d1, l1, p1], birth), Predicate([d2, l2, p1], birth), Predicate([d1, d2], different)], Predicate([p1, d1, d2], error_multi_birth)]]
DEATH_MULTITIMES = [[[Predicate([d1, l1, p1], death), Predicate([d2, l2, p1], death), Predicate([d1, d2], different)], Predicate([p1, d1, d2], error_multi_death)]]

DEATH_BIRTH_RULES = [[[Predicate([d1, l1, p1], birth), Predicate([d2, l2, p1], death), Predicate([d2, d1], before)],
     Predicate([p1, d1, d2], error_date)]]
    # [[Predicate([y, x], before)], Predicate([x, y], after)],
    #  [[Predicate([y, x], after)], Predicate([x, y], before)],


B_RULES = [BIRTH_MULTITIMES, DEATH_MULTITIMES, DEATH_BIRTH_RULES]

# Rules
ENCOUNTER_RULES = [
    [[Predicate([d1, l1, p1, p2], encounter), Predicate([d1, l2, p1], position),
      Predicate([l1, l2], far)],
     Predicate([d1, l1, l2, p1, p2], warning_encounter)],
    [[Predicate([d1, l1, p1, p2], encounter), Predicate([d1, l2, p2], position),
      Predicate([l1, l2], far)],
     Predicate([d1, l1, l2, p1, p2], warning_encounter)]]


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

ELECTION_BEFORE_BIRTH = [
    [[Predicate([d1, l1, p1], birth), Predicate([d2, l2, p1], death), Predicate([d3, l3, p1], election),
      Predicate([d3, d1], before)], Predicate([d1, d2, d3, l1, l2, l3, p1], error_election)]
]

ELECTION_AFTER_DEATH = [
    [[Predicate([d1, l1, p1], birth), Predicate([d2, l2, p1], death), Predicate([d3, l3, p1], election),
      Predicate([d2, d3], before)], Predicate([d1, d2, d3, l1, l2, l3, p1], error_election)]
]

GRANDFATHER_RULES = [
    [[Predicate([p1, p2], son)], Predicate([p2, p1], father)],
    [[Predicate([p1, p2], father), Predicate([p2, p3], father)], Predicate([p1, p3], grandfather)]
]

# Rules
MARIAGE_RULES = [
    #dates for only one person available
    [[Predicate([d1, l1, p1], birth), Predicate([d2, l2, p1], death),  Predicate([d3, l3, p1, p2], mariage), Predicate([d3, d1], before)],
    Predicate([d1, d2, d3, l1, l2, l3, p1, p2], error_mariage)],
    [[Predicate([d1, l1, p1], birth), Predicate([d2, l2, p1], death), Predicate([d3, l3, p1, p2], mariage), Predicate([d2, d3], before)],
    Predicate([d1, d2, d3, l1, l2, l3, p1, p2], error_mariage)],
    #second person
    [[Predicate([d1, l1, p2], birth), Predicate([d2, l2, p2], death),  Predicate([d3, l3, p1, p2], mariage), Predicate([d3, d1], before)],
    Predicate([d1, d2, d3, l1, l2, l3, p2, p1], error_mariage)],
    [[Predicate([d1, l1, p2], birth), Predicate([d2, l2, p2], death), Predicate([d3, l3, p1, p2], mariage), Predicate([d2, d3], before)],
    Predicate([d1, d2, d3, l1, l2, l3, p2, p1], error_mariage)]
]

MARIAGE_BEFORE_BIRTH = [
    [[Predicate([d1, l1, p1], birth), Predicate([d2, l2, p1], death),  Predicate([d3, l3, p1, p2], mariage), Predicate([d3, d1], before)],
    Predicate([d1, d2, d3, l1, l2, l3, p1, p2], error_mariage)]
]

MARIAGE_AFTER_DEATH = [
    [[Predicate([d1, l1, p1], birth), Predicate([d2, l2, p1], death), Predicate([d3, l3, p1, p2], mariage), Predicate([d2, d3], before)],
    Predicate([d1, d2, d3, l1, l2, l3, p1, p2], error_mariage)]
]

#Rules
DIVORCE_RULES = [
    [[Predicate([d1, l1, p1, p2], mariage), Predicate([d2, l2, p1, p3], mariage), Predicate([d1, d2], before)],
    Predicate([d1, d2, l1, l2, p1, p2, p3], divorce)]
]

# Rule ideas:
    #Date de Distinction > Date naissance
    #Date d'Election > Date naissance et < Date mort
    #Naissance enfant > naissance personne en question
    #Hypermot nécessitant un nom mais qui n'est pas suivi d'un nom (naissance sans nom de l'enfant, election, ...)
    #Autres pages intéressantes : Mariage, démission, nomination, participation
