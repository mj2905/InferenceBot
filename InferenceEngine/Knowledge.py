class KnowledgeBase:
    """ Une base de connaissances destinée à contenir les faits et les\ 
        règles d'un système de chaînage avant.
    """

    def __init__(self, builderOfRule):
        """ Construit une base de connaissances.

            Le paramètre ``constructeur_de_regle`` doit être une fonction\ 
            prenant deux arguments : la liste des conditions d'une règle et sa\
            conclusion. La fonction doit retourner une règle du type désiré.

            :param contructeur_de_regle: une fonction construisant une règle.
        """

        self.facts = []
        self.rules = []
        self.builderOfRule = builderOfRule

    def addFact(self, fait):
        """ Ajoute un fait dans la base de connaissances. 

            :param fait: un fait.
        """

        self.facts.append(fait)

    def addFacts(self, faits):
        """ Ajoute une liste de faits dans la base de connaissances.

            :param list faits: une liste de faits.
        """

        self.facts.extend(faits)

    def addRule(self, description):
        """ Ajoute une règle dans la base de connaissances étant donné sa\
            description.

            Une règle est décrite par une liste (ou un tuple) de deux\
            éléments : une liste de conditions et une conclusion.

            Les conditions et la conclusion doivent être des propositions.

            :param description: une description de règle.
        """

        regle = self.builderOfRule(description)
        self.rules.append(regle)

    def addRules(self, descriptions):
        """ Ajoute des règles dans la base de connaissances.

            L'argument est une liste de descriptions, chacune composée d'une\
            liste de conditions et d'une conséquence.

            :param list descriptions: une liste de descriptions de règles.
        """

        for description in descriptions:
            self.addRule(description)
