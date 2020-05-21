import requests
import operator
# from csense.mining.node import *
# from csense.parser.context import *

mem = {}

def lookup(word):
    if word in mem:
        return mem[word]
    # url = "http://ec2-54-164-171-68.compute-1.amazonaws.com/c/en/" + word + "?offset=0&limit=10000"
    url = "http://localhost/c/en/" + word + "?offset=0&limit=10000"
    # url = "http://conceptnet5.media.mit.edu/data/5.4/c/en/" + word + "?offset=0&limit=10000"
    obj = requests.get(url).json()
    # print(obj)
    edgeNames = set()
    edges = []
    for edge in obj['edges']:
        start_term = edge['start']['term'].split('/')[-1]
        end_term = edge['end']['term'].split('/')[-1]
        if edge['start'].get('language') and edge['start']['language'] == 'en' and start_term != word:
            if start_term not in edgeNames:
                node = Edge(start_term, edge['weight'], edge['rel']['label'], 'start')
                edges.append(node)
            edgeNames.add(start_term)

        elif edge['end'].get('language') and edge['end']['language'] == 'en' and end_term != word:
            if end_term not in edgeNames:
                node = Edge(end_term, edge['weight'], edge['rel']['label'], 'end')
                edges.append(node)
            edgeNames.add(end_term)

    edges.sort(key=operator.attrgetter('weight'), reverse = True)
#     for node in edges:
#         print(node)
#     print(len(edges))
    mem[word] = edges
    return edges


def search(word):
    # url = "http://conceptnet5.media.mit.edu/data/5.4/c/en" + word + "?rel=/r/AtLocation&limit=1000"
    # url = "http://conceptnet5.media.mit.edu/data/5.4/search?rel=/r/AtLocation&start=/c/en/" + word + "&limit=1000"
    # url1 = "http://conceptnet5.media.mit.edu/data/5.4/search?rel=/r/AtLocation&end=/c/en/" + word + "&limit=1000"
    # url = "http://localhost/search?rel=/r/AtLocation&end=/c/en/" + word + "&limit=1000"
    url = "http://localhost/search?rel=/r/AtLocation&end=/c/en/" + word + "&limit=1000"
    obj = requests.get(url).json()
    #obj1 = requests.get(url1).json()
    obj1 = obj

    # print(obj['edges'])
    # print(len(obj['edges']))

    # for edge in obj['edges']:
    #     print(edge)
    #     meaning = edge['start']['@id'].split('/')
    #     if 'en' in meaning:
    #         print(meaning, edge['weight'])

    # for edge in obj1['edges']:
    #     print(edge)
    #     meaning = edge['start']['@id'].split('/')
    #     if 'en' in meaning:
    #         print(meaning, edge['weight'])

        # print(meaning[-1])
        # print(edge['end']['@id'])

    edgeNames = set()
    for edge in obj['edges']:
        start_term = edge['start']['term'].split('/')[-1]
        end_term = edge['end']['term'].split('/')[-1]
        if edge['start'].get('language') and edge['start']['language'] == 'en' and start_term != word:
            # if start_term not in edgeNames:
            #     node = Edge(start_term, edge['weight'], edge['rel']['label'], 'start')
            #     edges.append(node)
            edgeNames.add(start_term.split('_')[-1])
            edgeNames.add(start_term)

        elif edge['end'].get('language') and edge['end']['language'] == 'en' and end_term != word:
            # if end_term not in edgeNames:
            #     node = Edge(end_term, edge['weight'], edge['rel']['label'], 'end')
            #     edges.append(node)
            edgeNames.add(start_term.split('_')[-1])
            edgeNames.add(end_term)

    for edge in obj1['edges']:
        start_term = edge['start']['term'].split('/')[-1]
        end_term = edge['end']['term'].split('/')[-1]
        if edge['start'].get('language') and edge['start']['language'] == 'en' and start_term != word:
            # if start_term not in edgeNames:
            #     node = Edge(start_term, edge['weight'], edge['rel']['label'], 'start')
            #     edges.append(node)
            # print(start_term)
            edgeNames.add(start_term)

        elif edge['end'].get('language') and edge['end']['language'] == 'en' and end_term != word:
            # if end_term not in edgeNames:
            #     node = Edge(end_term, edge['weight'], edge['rel']['label'], 'end')
            #     edges.append(node)
            # print(end_term)
            edgeNames.add(end_term)
    # print(edgeNames)
    return edgeNames

def relatedness(node1, node2):
    url = "http://conceptnet5.media.mit.edu/data/5.4/relatedness?node1=/c/en/" + node1 + "&node2=/c/en/" + node2
    obj = requests.get(url).json()
    print(obj)

def related(node):
    url = "http://conceptnet5.media.mit.edu/data/5.4//related/c/en/" + node
    obj = requests.get(url).json()
    # print(obj)
    return obj


# print(search("barbeque"))
# print(search("backyard"))
# relatedness("bowl", "cup")
# relatedTerms = related("glass")['related']
# for term in relatedTerms:
#     print(term)
