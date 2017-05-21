from Scraping.WikiStrings import *

def modifyURLToDiscussion(urls):
    result = set()
    for url in urls:
        i = url.rfind("/")
        if i == -1:
            continue
        result.add("Discussion:" + url[i+1:])
    return result

def pretty(list_facts, allLinks):
    list_pretty = []
    pagesWithSomething = set()

    for elem in list_facts:

        string = None

        if ERROR_DATE in elem.name:
            string = (elem.name + " : [[" + elem.propositions[0].name + "]] né en " + elem.propositions[1].name
                + " et mort en " + elem.propositions[2].name)
        elif WARNING_ENCOUNTER in elem.name:
            string = (elem.name + " : [[" + elem.propositions[3].name + "]] et [[" + elem.propositions[4].name
                + "]] se sont rencontrés à [[" + elem.propositions[1].name + "]] et à [[" + elem.propositions[2].name
                + "]] en même temps à la date " + elem.propositions[0].name)
        elif ERROR_BIRTH in elem.name:
            string = (elem.name + " : [[" + elem.propositions[0].name + "]] né en " + elem.propositions[1].name
                + " et né en " + elem.propositions[2].name)
        elif ERROR_DEATH in elem.name:
            string = (elem.name + " : [[" + elem.propositions[0].name + "]] mort en "
                + elem.propositions[1].name + " et mort en " + elem.propositions[2].name)
        elif ERROR_ELECTION in elem.name:
            string = (elem.name + " : [[" + elem.propositions[6].name + "]] (" + elem.propositions[0].name
                + " / " + elem.propositions[1].name + ")"+ " est élu en " + elem.propositions[2].name + " à [[" + elem.propositions[5].name + "]]")
        elif ERROR_MARIAGE in elem.name:
            string = (elem.name + " : [[" + elem.propositions[6].name + " ]] (" + elem.propositions[0].name
                + " / " + elem.propositions[1].name + ") et " + elem.propositions[7].name + " se marient le "
                + elem.propositions[2].name + " à [[" + elem.propositions[5].name + "]]")
        elif DIVORCE_INFERENCE in elem.name:
            string = (elem.name + " : [[" + elem.propositions[4].name + "]] se marie avec [[" + elem.propositions[5].name + "]] en "
            + elem.propositions[0].name + " puis avec [[" + elem.propositions[6].name + "]] en " + elem.propositions[1].name)

        if string is not None:
            list_pretty.append((string, modifyURLToDiscussion(elem.urls)))
            pagesWithSomething = pagesWithSomething.union(elem.urls)

    pagesWithNothing = set([filteredUrl for url in allLinks if url not in pagesWithSomething
                                            for filteredUrl in modifyURLToDiscussion(set([url]))])

    return (list_pretty, pagesWithNothing)
