from Predicate import Atom, Predicate
from Unificator import Unificator


x = Atom('x',True)
y = Atom('y',True)
z = Atom('z',True)


a = Atom('dolan',False)
b = Atom('goofy',False)
c = Atom('toto',False)

prop1 = Predicate([x,a],'friend')
prop2 = Predicate([b,a],'friend')
unificateur = Unificator()

print(prop2)
v = unificateur.pattern_match(prop1, prop2)
print(v)