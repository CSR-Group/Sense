import requests
import operator
from csense.mining.node import *

def lookup(word):
    url = "http://conceptnet5.media.mit.edu/data/5.4/c/en/" + word + "?offset=0&limit=10000"
    obj = requests.get(url).json()
    # print(obj)
    edgeNames = set()
    edges = []
    for edge in obj['edges']:
        # print(edge)
        if edge['start'].get('language') and edge['start']['language'] == 'en' and edge['rel']['label'] == "RelatedTo" and edge['start']['label'] != word:
            if edge['start']['label'] not in edgeNames:
                node = Edge(edge['start']['label'], edge['weight'], edge['rel']['label'], 'start')
                edges.append(node)
            edgeNames.add(edge['start']['label'])

        elif edge['end'].get('language') and edge['end']['language'] == 'en' and edge['rel']['label'] == "RelatedTo" and edge['end']['label'] != word:
            if edge['end']['label'] not in edgeNames:
                node = Edge(edge['end']['label'], edge['weight'], edge['rel']['label'], 'end')
                edges.append(node)
            edgeNames.add(edge['end']['label'])

    edges.sort(key=operator.attrgetter('weight'), reverse = True)
    # for node in edges:
    #     print(node)
    # print(len(edges))
    return edges

def search(word):
    url = "http://conceptnet5.media.mit.edu/data/5.4/search?rel=/r/RelatedTo&end=/c/en/" + word + "&limit=1000"
    obj = requests.get(url).json()
    # print(obj['edges'])
    print(len(obj['edges']))
    for edge in obj['edges']:
        print(edge)
        meaning = edge['start']['@id'].split('/')
        if 'en' in meaning:
            print(meaning, edge['weight'])

        # print(meaning[-1])
        # print(edge['end']['@id'])

def relatedness(node1, node2):
    url = "http://conceptnet5.media.mit.edu/data/5.4/relatedness?node1=/c/en/" + node1 + "&node2=/c/en/" + node2
    obj = requests.get(url).json()
    print(obj)

def related(node):
    url = "http://conceptnet5.media.mit.edu/data/5.4//related/c/en/" + node
    obj = requests.get(url).json()
    # print(obj)
    return obj

# search("scuttlebutt")
# relatedness("coffee_pot", "tea_kettle")
# relatedTerms = related("glass")['related']
# for term in relatedTerms:
#     print(term)

def getNodes():
    nodeQueue = []
    candidates = ['refrigerator', 'table', 'dishwasher', 'water cooler', 'dining room']
    for candidate in candidates:
        print(candidate.replace(' ','_'))
        edges = lookup(candidate.replace(' ','_'))
        node = Node(candidate,edges,-1)
        nodeQueue.append(node)
        print(node)

getNodes()
# lookup("glass")