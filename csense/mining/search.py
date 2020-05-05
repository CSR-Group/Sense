from csense.mining.node import *
from csense.parser.sentence import parse
from queue import PriorityQueue
from csense.mining.conceptnet import lookup

import spacy
nlp = spacy.load("en_core_web_sm")

# Hyper-Parameters
DEFAULT_CANDIDATE_NODE_HEURISTIC_WEIGHT = 1000000
DEFAULT_QUESTION_NODE_HEURISTIC_WEIGHT = 1000000
SEARCH_STOP_WORDS = False
TOP_N_EDGES = 20

# Populating nodeQueue for BFS
CANDIDATE_NODE_TYPE = "CANDIDATE"
QUESTION_NODE_TYPE = "QUESTION"

class HeuristicSearch:

    def __init__(self, parsedSentence):

        self.nodeQueue = PriorityQueue()
        self.visited = set()

        for candidate in parsedSentence.candidates:
            self.addInitialEntitiesToQueue(candidate, CANDIDATE_NODE_TYPE, DEFAULT_CANDIDATE_NODE_HEURISTIC_WEIGHT)

        for context in parsedSentence.contexts:
            # Adding Subjects to Node Queue
            for subject in context.subjects:
                if not subject.is_stop_word or SEARCH_STOP_WORDS:
                    self.addInitialEntitiesToQueue(subject.name, QUESTION_NODE_TYPE, DEFAULT_QUESTION_NODE_HEURISTIC_WEIGHT)

            # Adding Action to Node Queue
            if not context.action.is_stop_word or SEARCH_STOP_WORDS:
                self.addInitialEntitiesToQueue(context.action.name, QUESTION_NODE_TYPE, DEFAULT_QUESTION_NODE_HEURISTIC_WEIGHT)

            # Adding Objects to Node Queue
            for obj in context.objects:
                if not obj.is_stop_word or SEARCH_STOP_WORDS:
                    self.addInitialEntitiesToQueue(obj.name, QUESTION_NODE_TYPE, DEFAULT_QUESTION_NODE_HEURISTIC_WEIGHT)

    def addInitialEntitiesToQueue(self, entity, type, weight):
        entity_name = entity.replace(' ', '_')
        doc = nlp(entity)
        postag = ''
        for token in doc:
            postag = token.pos_
        node = Node(entity_name, postag, type, weight, 0)
        self.nodeQueue.put(node)

    def run(self, depth_limit=2):

        while not self.nodeQueue.empty():

            frontierNode = self.nodeQueue.get()

            if frontierNode.name in self.visited:
                continue

            if frontierNode.depth != depth_limit:
                print("Exploring  - ", frontierNode.name)
                edges = lookup(frontierNode.name)[0:TOP_N_EDGES]
                print("Edges  - ", str([str(edge) for edge in edges]))

                weight_sum = self.getWeightSum(edges)
                for edge in edges:
                    weight = frontierNode.weight * (edge.weight / weight_sum)
                    node = Node(edge.name,
                                self.getPosTag(edge.name),
                                frontierNode.nodeType,
                                weight,
                                frontierNode.depth + 1)
                    self.nodeQueue.put(node)

    def getPosTag(self, tokens):
        postag = ""
        for token in nlp(tokens):
            postag = token.pos_
        return postag

    def getWeightSum(self, edges):
        sum = 0
        for edge in edges:
            sum += edge.weight
        return sum

