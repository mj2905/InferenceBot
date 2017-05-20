import graphviz as gv


class GenealogyTreeGenerator:
    def __init__(self, urls=None):
        if urls is None:
            urls = []
        self.graph = gv.Graph(format='png')
        self.members = []
        self.urls = urls

    def addUrl(self, url):
        self.urls.extend(url)

    def addMember(self, person):

        if person not in self.members:
            if person.sex == 'M':
                self.graph.attr('node', shape='box', color='red')
            elif person.sex == 'F':
                self.graph.attr('node', shape='box', color='blue')
            else:
                self.graph.attr('node', shape='box', color='black')

            self.members.append(person)
            self.graph.node(person.__str__())

    def addMembers(self, members):
        for member in members:
            self.addMember(member)

    def getMemberFromName(self, name):
        for member in self.members:
            if member.__str__() == name:
                return member

    def addPartner(self, person1, person2):
        self.addMembers([person1, person2])

        namePartner1 = person1.__str__()
        namePartner2 = person2.__str__()

        self.graph.attr('node', shape='point', color='black')
        partner = self.getMemberFromName(namePartner1)
        self.getMemberFromName(namePartner2).childNum = partner.childNum
        self.getMemberFromName(namePartner2).addChild()

        if not partner.hasChild:
            self.graph.node(partner.childNum)
            self.graph.edge(namePartner1, partner.childNum)
            partner.addChild()

        self.graph.edge(namePartner2, partner.childNum)

    def addChild(self, parent, child):
        self.addMembers([parent, child])

        nameParent = parent.__str__()
        nameChild = child.__str__()

        self.graph.attr('node', shape='point', color='black')
        parent = self.getMemberFromName(nameParent)

        if not parent.hasChild:
            self.graph.node(parent.childNum)
            self.graph.edge(nameParent, parent.childNum)
            parent.addChild()

        self.graph.edge(parent.childNum, nameChild)

    def render(self, filename):
        self.graph.render(filename)
