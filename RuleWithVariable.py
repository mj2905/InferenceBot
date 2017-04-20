class RuleWithVariable:
    """ Représentation d'une règle d'inférence pour le chaînage avec\
        variables.
    """

    def __init__(self, conditions, conclusion):
        """ Construit une règle étant donné une liste de conditions et une\
            conclusion.
            
            :param list conditions: une collection de propositions (pouvant\
            contenir des variables) nécessaires à déclencher la règle.
            :param conclusion: la proposition (pouvant contenir des variables)\
            résultant du déclenchement de la règle.
        """

        self.conditions = conditions
        self.conclusion = conclusion

    def dependsOf(self, fact, method):
        """ Vérifie qu'un fait fait partie, sous réserve de substitution,\
            des conditions de la règle.
            
            :param fact: un fait qui doit faire partie des conditions de\
            déclenchement.
            :param method: ``Filtre`` ou ``Unificateur``, détermine le type\
             de pattern match à appliquer.
            :return: un dictionnaire qui attribue un environnement à chaque\
            condition qui peut être satisfaite par le fait pasée en paramètre.\
            ``False`` si aucune condition n'est satisfaite par le fait.
        """
        envs = {}

        for condition in self.conditions:
            # Si au moins une des conditions retourne un environnement,
            # nous savons que la proposition satisfait une des conditions.
            env = method.pattern_match(fact, condition, {})
            if env != method.failure:
                envs[condition] = env

        return envs

    def satisfiedBy(self, facts, cond, env, method):
        """ Vérifie que des faits suffisent, sous réserve de substitution,\
            à déclencher la règle.

            :param list facts: une liste de faits.
            :param cond: la condition qui a donné lieu à ``env`` par le\
            pattern match.
            :param dict env: un environnement de départ déjà établi par\
            ``depend_de``.
            :param method: ``Filtre`` ou ``Unificateur``, détermine le type\
             de pattern match à appliquer.
            :return: une liste d'environnements qui correspondent à toutes les\
            substitutions possibles entre les conditions de la règle et les\
            propositions. On retourne une liste vide si au moins une condition\
            ne peut être satisfaite.
        """
        envs = [env]

        # On n'a pas besoin de tester ``cond`` car cela a été fait dans l'appel
        # à ``depend_de`` qui précède l'appel à cette méthode.
        conditions_a_tester = [cond1 for cond1 in self.conditions if cond1 != cond]

        # Pour chaque condition dans la liste des conditions, si la liste
        # des environnements n'est pas vide, on y ajoute les environnements
        # qui permettent de satisfaire une des conditions.
        for cond1 in conditions_a_tester:
            envs_nouveaux = []

            for facts in facts:
                for env1 in envs:
                    env1 = method.pattern_match(facts, cond1, env1)
                    if env1 != method.failure:
                        envs_nouveaux.append(env1)

            # Si au moins une condition n'est pas satisfaite, la règle ne l'est pas non plus.
            if len(envs_nouveaux) == 0:
                return []

            envs = envs_nouveaux

        return envs

    def __repr__(self):
        """ Représentation d'une règle sous forme de string. """

        return '{} => {}'.format(str(self.conditions), str(self.conclusion))