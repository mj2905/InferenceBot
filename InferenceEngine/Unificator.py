from InferenceEngine.Predicate import Predicate


class Unificator:
    """ Classe implémentant les méthodes de l'unification de propositions avec\
        variables. """

    failure = 'failure'

    def substitute(self, pattern, env):
        """ Effectue des substitutions de variables dans un pattern.
            
            :param pattern: une proposition dont les variables doivent être\
            remplacées par d'autres propositions.
            :param dict env: un environnment, c'est-à-dire un dictionnaire de\
            substitutions ``{variable : proposition}``.
            :return: le pattern dont les variables ont été remplacées les\
            propositions qui leur sont associées dans l'environnement.
        """
        if pattern.getIsAtomic():
            if pattern in env:
                return self.substitute(env[pattern], env)
            else:
                return pattern

        pattern_subst = Predicate([], pattern.name)

        for sub_pattern in pattern.propositions:
            sub_pattern_subst = self.substitute(sub_pattern, env)
            pattern_subst.add(sub_pattern_subst)

        return pattern_subst

    def unify(self, prop1, prop2):
        """ Effectue l'unification entre deux propositions.

            :param prop1: une proposition pouvant contenir des variables.
            :param prop2: une proposition pouvant contenir des variables.
            :return: un environnment, c'est-à-dire un dictionnaire de\
            substitutions ``{variable : proposition}``, ou ``'échec'`` si\
            l'unification a échoué.
        """
        if len(prop1) != len(prop2):
            return Unificator.failure

        if isinstance(prop1, Predicate) and isinstance(prop2, Predicate) and prop1.name != prop2.name:
            return Unificator.failure

        if len(prop1) == 0 and len(prop2) == 0:
            return {}
        if len(prop1) == 0 or len(prop2) == 0:
            return Unificator.failure

        # Une des deux propositions est un atome => on essaie de le matcher.
        if prop1.getIsAtomic() or prop2.getIsAtomic():
            if prop1 == prop2:
                return {}

            if not prop1.getIsAtomic():
                prop1, prop2 = prop2, prop1

            if prop1.getIsVariable():
                if prop1 in prop2:
                    return Unificator.failure
                else:
                    return {prop1.atom(): prop2.atom()}

            if prop2.getIsVariable():
                return {prop2.atom(): prop1.atom()}

            # Dans les autres cas, l'unification est un échec.
            return Unificator.failure

        # Aucune des propositions n'est atomique : on unifie récursivement.
        prop1_head = prop1.head()
        prop2_head = prop2.head()
        prop1_tail = prop1.tail()
        prop2_tail = prop2.tail()
        head_env = self.unify(prop1_head, prop2_head)
        if head_env == Unificator.failure:
            return Unificator.failure

        prop1_tail = self.substitute(prop1_tail, head_env)
        prop2_tail = self.substitute(prop2_tail, head_env)
        reste_env = self.unify(prop1_tail, prop2_tail)
        if reste_env == Unificator.failure:
            return Unificator.failure
        #print()
        head_env.update(reste_env)
        return head_env

    def pattern_match(self, prop1, prop2, env=None):
        """ Effectue l'unification en tenant compte d'un environnement initial.

            :param prop1: une proposition pouvant contenir des variables.
            :param prop2: une proposition pouvant contenir des variables.
            :param dict env: l'environnement initial à prendre en compte.
            :return: un nouvel environnment ou ``'échec'``.
        """
        if env is not None:
            prop1 = self.substitute(prop1, env)
            prop2 = self.substitute(prop2, env)
            env = env.copy()
        else:
            env = {}

        resultat = self.unify(prop1, prop2)
        if resultat == Unificator.failure:
            return Unificator.failure

        env.update(resultat)
        return env
