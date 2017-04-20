""" Fonctions utilitaires pour gérer des propositions sans ou avec variables\
    dans un moteur d'inférence.
"""
from abc import ABCMeta, abstractmethod


class Proposition(metaclass=ABCMeta):
    @abstractmethod
    def atom(self):
        pass

    @abstractmethod
    def getIsAtomic(self):
        pass

    @abstractmethod
    def getIsVariable(self):
        pass

    @abstractmethod
    def __len__(self):
        pass

    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def __hash__(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def __contains__(self, item):
        pass


class Atom(Proposition):
    def __init__(self, name, isVariable):
        self.name = name
        self.isVariable = isVariable

    def atom(self):
        return self

    def getIsAtomic(self):
        return True

    def getIsVariable(self):
        return self.isVariable

    def __len__(self):
        return 1

    def __eq__(self, other):
        return self.name == other.name and self.isVariable == other.isVariable

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return self.name

    def __contains__(self, item):
        return self == item


class Predicate(Proposition):
    def __init__(self, propositions, name):
        self.propositions = propositions
        self.name = name

    def atom(self):
        if self.getIsAtomic():
            return self.propositions[0]

    def getIsVariable(self):
        return len(self.propositions) == 1 and self.propositions[0].getIsVariable()

    def getIsAtomic(self):
        return len(self.propositions) == 1 and self.propositions[0].getIsAtomic()

    def head(self):
        if self.getIsAtomic():
            raise Exception("Proposition atomique: Impossible de la segmenter.")
        elif len(self.propositions) > 0:
            return self.propositions[0]
        else:
            raise Exception("Proposition vide: Impossible de la segmenter.")

    def tail(self):
        """ Coupe la proposition courante et retourne la portion située après le\
            premier élément.

            A noter que dans le cas d'une proposition atomique, la méthode soulève\
            une exception.

            :param proposition: une proposition.
            :return: le corps de la proposition composée.
        """

        if self.getIsAtomic():
            raise Exception("Proposition atomique: Impossible de la segmenter.")
        elif len(self.propositions) > 0:
            return Predicate(self.propositions[1:], name=self.name)
        else:
            raise Exception("Proposition vide: Impossible de la segmenter.")

    def list_variable(self):
        variables = set()
        if self.getIsAtomic():
            if self.getIsVariable():
                variables.add(self.propositions)
        else:
            for sous_prop in self.propositions:
                variables.update(sous_prop.list_variable())
        return variables

    def add(self, proposition):
        if self.propositions is None:
            self.propositions = [proposition]
        else:
            self.propositions.append(proposition)

    def __len__(self):
        return len(self.propositions)

    def __eq__(self, other):
        return self.propositions == other.propositions

    def __hash__(self):
        return hash(frozenset(self.propositions))

    def __repr__(self):
        res = self.name + '('
        for p in self.propositions:
            res = res + p.name + ','
        return res[:len(res) - 1] + ')'

    def __contains__(self, item):
        return set(item.propositions) < set(self.propositions)
