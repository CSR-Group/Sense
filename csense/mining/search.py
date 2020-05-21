from csense.mining.node import *
from csense.parser.sentence import parse
from queue import PriorityQueue
from csense.mining.conceptnet import lookup
from csense.mining.conceptnet import relatedness

import spacy
nlp = spacy.load("en_core_web_sm")

# Hyper-Parameters
DEFAULT_CANDIDATE_NODE_HEURISTIC_WEIGHT = 1000000
DEFAULT_QUESTION_NODE_HEURISTIC_WEIGHT = 1000000
SEARCH_STOP_WORDS = False
TOP_N_EDGES = 20

# Populating nodeQueue for BFS


class RelatednessSearch:

    def __init__(self, parsedSentence):

        self.candidates = []
        self.candidateScore = {}
        self.parsedSentence = parsedSentence

        for candidate in parsedSentence.candidates:
            self.candidates.append(candidate)
            self.candidateScore[candidate] = 0

    def run(self):
        for context in self.parsedSentence.contexts:
            for subject in context.subjects:
                if not subject.is_stop_word or SEARCH_STOP_WORDS:
                    for candidate in self.candidates:
                        self.candidateScore[candidate] += relatedness(candidate, subject.name)

            if not context.action.is_stop_word or SEARCH_STOP_WORDS:
                for candidate in self.candidates:
                    self.candidateScore[candidate] += relatedness(candidate, context.action.name)

            for obj in context.objects:
                if not obj.is_stop_word or SEARCH_STOP_WORDS:
                    for candidate in self.candidates:
                        self.candidateScore[candidate] += relatedness(candidate, obj.name)

        max_score = -1
        max_candidate = None
        for candidate in self.candidates:
            if self.candidateScore[candidate] > max_score:
                max_score = self.candidateScore[candidate]
                max_candidate = candidate
            # print(candidate, " - ", self.candidateScore[candidate])

        return max_candidate

class HeuristicSearch:

    def __init__(self, parsedSentence):

        self.nodeQueue = PriorityQueue()
        self.visited = set()

        self.candidates = []
        self.candidateScore = {}
        self.candidateNodes = {}
        self.candidateWeightByNode = {}

        for candidate in parsedSentence.candidates:
            self.candidates.append(candidate)
            self.candidateScore[candidate] = 0

        # for candidate in parsedSentence.candidates:
        #     self.candidateScore[candidate] = 0
        #     self.candidateNodes[candidate] = set()
        #     self.addInitialEntitiesToQueue(candidate, CANDIDATE_NODE_TYPE, DEFAULT_CANDIDATE_NODE_HEURISTIC_WEIGHT)

        for context in parsedSentence.contexts:
            # Adding Subjects to Node Queue
            for subject in context.subjects:
                if not subject.is_stop_word or SEARCH_STOP_WORDS:
                    self.nodeQueue.put(self.getInitialEntity(subject.name,
                                                             QUESTION_NODE_TYPE,
                                                             DEFAULT_QUESTION_NODE_HEURISTIC_WEIGHT))
                # Adding properties to Node Queue
                propKeys  = subject.properties.keys()
                prop = subject.properties
                for key in propKeys:
                    for val in prop[key]:
                        self.nodeQueue.put(self.getInitialEntity(val,
                                                                QUESTION_NODE_TYPE,
                                                                DEFAULT_QUESTION_NODE_HEURISTIC_WEIGHT))


            # Adding Action to Node Queue
            if not context.action.is_stop_word or SEARCH_STOP_WORDS:
                self.nodeQueue.put(self.getInitialEntity(context.action.name,
                                                         QUESTION_NODE_TYPE,
                                                         DEFAULT_QUESTION_NODE_HEURISTIC_WEIGHT))

            # Adding Objects to Node Queue
            for obj in context.objects:
                if not obj.is_stop_word or SEARCH_STOP_WORDS:
                    self.nodeQueue.put(self.getInitialEntity(obj.name,
                                                             QUESTION_NODE_TYPE,
                                                             DEFAULT_QUESTION_NODE_HEURISTIC_WEIGHT))
                # Adding properties to Node Queue
                propKeys  = obj.properties.keys()
                prop = obj.properties
                for key in propKeys:
                    for val in prop[key]:
                        self.nodeQueue.put(self.getInitialEntity(val,
                                                                QUESTION_NODE_TYPE,
                                                                DEFAULT_QUESTION_NODE_HEURISTIC_WEIGHT))

    def getInitialEntity(self, entity, type, weight):
        entity_name = entity.replace(' ', '_')
        doc = nlp(entity)
        postag = ''
        for token in doc:
            postag = token.pos_
        node = Node(entity_name, postag, type, weight, 0, entity_name)
        return node

    def run(self, candidateDepthLimit = 2, questionDepthlimit = 2) :

        for candidate in self.candidates:
            self.candidateSearch(candidate, candidateDepthLimit)

        self.questionSearch(questionDepthlimit)

        # print("--------")
        max_score = -1
        max_candidate = None
        for candidate in self.candidates:
            if self.candidateScore[candidate] > max_score:
                max_score = self.candidateScore[candidate]
                max_candidate = candidate
            # print(candidate, " - ", self.candidateScore[candidate])

        return max_candidate


    def candidateSearch(self, candidate, candidateDepthLimit):

        queue = PriorityQueue()
        weightByNodeMap = {}
        queue.put(self.getInitialEntity(candidate, CANDIDATE_NODE_TYPE, DEFAULT_CANDIDATE_NODE_HEURISTIC_WEIGHT))

        while not queue.empty():
            frontierNode = queue.get()

            if frontierNode.name in weightByNodeMap:
                continue
            weightByNodeMap[frontierNode.name] = frontierNode.weight

            if frontierNode.depth < candidateDepthLimit:
                # print("Exploring  - ", frontierNode.name, " - ", frontierNode.weight)
                edges = lookup(frontierNode.name)[0:TOP_N_EDGES]
                # print("Edges  - ", str([str(edge) for edge in edges]))

                weight_sum = self.getWeightSum(edges)

                for edge in edges:
                    weight = frontierNode.weight * (edge.weight / weight_sum)
                    node = Node(edge.name,
                                self.getPosTag(edge.name),
                                frontierNode.nodeType,
                                weight,
                                frontierNode.depth + 1,
                                frontierNode.rootParent)
                    queue.put(node)

        self.candidateWeightByNode[candidate] = weightByNodeMap


    def questionSearch(self, depth_limit=2):

        visited = set()

        while not self.nodeQueue.empty():

            frontierNode = self.nodeQueue.get()

            # candidate scoring
            for candidate in self.candidates:
                if frontierNode.name in self.candidateWeightByNode[candidate]:
                    # candidateWeight = self.candidateWeightByNode[candidate][frontierNode.name]
                    # score = candidateWeight + frontierNode.weight
                    # self.candidateScore[candidate] = self.candidateScore[candidate] + score
                    self.candidateScore[candidate] = frontierNode.weight

            # Skip exploring if visited
            if frontierNode.name in visited:
                continue
            visited.add(frontierNode.name)

            # Explore
            if frontierNode.depth < depth_limit:
                # print("Exploring  - ", frontierNode.name , " - ", frontierNode.weight)
                edges = lookup(frontierNode.name)[0:TOP_N_EDGES]
                # print("Edges  - ", str([str(edge) for edge in edges]))

                weight_sum = self.getWeightSum(edges)
                for edge in edges:
                    weight = frontierNode.weight * (edge.weight / weight_sum)
                    node = Node(edge.name,
                                self.getPosTag(edge.name),
                                frontierNode.nodeType,
                                weight,
                                frontierNode.depth + 1,
                                frontierNode.rootParent)
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

