from InferenceEngine.Predicate import Atom, Predicate

# Date Variables
from Scraping import WikiStrings

d1 = Atom('d1', True)
d2 = Atom('d2', True)

# Location Variables
l1 = Atom('l1', True)
l2 = Atom('l2', True)
l3 = Atom('l3', True)

# Person Variables
p1 = Atom('p1', True)
p2 = Atom('p2', True)

# Name of Predicate
before = WikiStrings.BEFORE
different = WikiStrings.DIFFERENT
#  after = WikiStrings.AFTER
birth = WikiStrings.BIRTH
death = WikiStrings.DEATH
error_date = WikiStrings.ERROR_DATE
encounter = WikiStrings.ENCOUNTER
position = WikiStrings.POSITION
# close = WikiStrings.CLOSE
far = WikiStrings.FAR
error_encounter = WikiStrings.ERROR_ENCOUNTER
error_multi_birth = WikiStrings.ERROR_BIRTH
error_multi_death = WikiStrings.ERROR_DEATH

# Rules

BIRTH_MULTITIMES = [[[Predicate([d1, l1, p1], birth), Predicate([d2, l2, p1], birth)], Predicate([d1, d2], different), Predicate([p1, d1, d2], error_multi_birth)]]
DEATH_MULTITIMES = [[[Predicate([d1, l1, p1], death), Predicate([d2, l2, p1], death)], Predicate([d1, d2], different), Predicate([p1, d1, d2], error_multi_death)]]

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
