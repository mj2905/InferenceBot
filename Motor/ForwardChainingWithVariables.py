from Motor.Chaining import Chaining
from Motor.Unificator import Unificator


class ForwardChainingWithVariables(Chaining):
    """ Un moteur d'inférence à chaînage avant avec variables. """

    def __init__(self, knowledge, method=None):
        """
            :param method: ``Filtre`` ou ``Unificateur``, détermine le type de\
            pattern match à appliquer. ``Filtre`` par défaut.
        """

        Chaining.__init__(self, knowledge)

        if method is None:
            self.method = Unificator()
        else:
            self.method = method

    def instanciateConclusion(self, regle, envs):
        """ Instancie la conclusion d'une règle pour tous les environnements.

            :param regle: la règle dont la conclusion doit être instanciée.
            :param list envs: les environnements servant à instancier la\
            conclusion.
            :return: une liste de propositions correspondant aux différentes\
            instanciations de la conclusion.
        """
        return [self.method.substitute(regle.conclusion, env) for env in envs]
    
    def chain(self):
        """ Effectue le chaînage avant sur les faits et les règles contenus\
            dans la base de connaissances.
        """
        queue = self.knowledge.facts[:]
        self.reset()

        while len(queue) > 0:
            fact = queue.pop(0)

            if fact not in self.solutions:
                self.trace.append(fact)
                self.solutions.append(fact)

                # Vérifie si des règles sont déclenchées par le nouveau fait.
                for rule in self.knowledge.rules:
                    cond_envs = rule.dependsOf(fact, self.method)
                    for cond, env in cond_envs.items():
                        # Remplace l'environnement par ceux qui satisfont
                        # toutes les conditions de la règle et pas seulement la 
                        # première condition.
                        envs = rule.satisfiedBy(self.solutions, cond, env, self.method)

                        # Ajoute la conclusion de la règle instanciée pour tous 
                        # les environnements possibles.
                        if len(envs) > 0:
                            queue.extend(self.instanciateConclusion(rule, envs))
                            self.trace.append(rule)

        return self.solutions