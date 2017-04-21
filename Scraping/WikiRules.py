from InferenceEngine.Predicate import Atom, Predicate

# Date Variables
from Scraping import WikiStrings

d1 = Atom('1', True)
l1 = Atom('2', True)

# Location Variables
d2 = Atom('3', True)
l2 = Atom('4', True)

# Person Variables
p = Atom('5', True)

# Name of Predicate
before = WikiStrings.BEFORE
#  after = WikiStrings.AFTER
birth = WikiStrings.BIRTH
death = WikiStrings.DEATH
error = WikiStrings.ERROR_DATE

# Rules
DEATH_BIRTH_RULES = [
    # [[Predicate([y, x], before)], Predicate([x, y], after)],
    #  [[Predicate([y, x], after)], Predicate([x, y], before)],
    [[Predicate([d1, l1, p], birth), Predicate([d2, l2, p], death), Predicate([d2, d1], before)],
     Predicate([p, d1, d2], error)]]
