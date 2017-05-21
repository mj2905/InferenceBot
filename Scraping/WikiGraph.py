from abc import ABCMeta, abstractmethod

from DataStructures.Datastructs import Wedding, Parent
from Scraping.GenealogyTreeGenerator import GenealogyTreeGenerator


class WikiGraph(metaclass=ABCMeta):
    def __init__(self):
        self.graphs = []

    @abstractmethod
    def addData(self, resData):
        pass

    @abstractmethod
    def generateGraph(self):
        pass


class WikiGenealogyTree(WikiGraph):
    def __init__(self):
        super().__init__()
        self.members = set()

    def addData(self, resData):
        members = set()
        for page in resData.data:
            temp = list(filter(lambda x: x is not None, page.weddings))
            if temp:
                for elem in temp:
                    members.add((elem, page.url))
        for page in resData.data:
            temp = list(filter(lambda x: x is not None, page.parents))
            if temp:
                for elem in temp:
                    members.add((elem, page.url))

        self.members = members

    def generateGraph(self):
        graphs = self.connected_components()
        for graph in graphs:
            g = GenealogyTreeGenerator()
            addedItems = set()
            childItems = set()
            for elem, url in graph:
                if elem not in addedItems:
                    if type(elem) == Wedding:
                        g.addPartner(elem.person1, elem.person2)
                    elif type(elem) == Parent:

                        alreadyChild = False

                        for parent, child in childItems:
                            if child == elem.person2:
                                alreadyChild = True
                        if not alreadyChild:
                            childItems.add((elem.person1, elem.person2))
                    addedItems.add(elem)
                g.addUrl(url)
            for p1, p2 in childItems:
                g.addChild(p1, p2)

            self.graphs.append(g)


    # The function to look for connected components.
    def connected_components(self):

        result = []
        nodes = set(self.members)

        while nodes:

            n = nodes.pop()
            group = {n}
            queue = [n]

            while queue:
                n = queue.pop(0)
                neighbors = self.links(n)
                neighbors.difference_update(group)
                nodes.difference_update(neighbors)
                group.update(neighbors)
                queue.extend(neighbors)
            result.append(group)

        return result

    def links(self, elemUrl):
        elem, url = elemUrl
        res = set()
        for member, url in self.members:
            if not elem.__eq__(member) and (elem.person1 in member.members() or elem.person2 in member.members()):
                res.add((member, url))
        return res
