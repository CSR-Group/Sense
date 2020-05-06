CANDIDATE_NODE_TYPE = "CANDIDATE"
QUESTION_NODE_TYPE = "QUESTION"

class Edge:

  def __init__(self, name, weight, rel, nodeType):
    self.name = name
    self.weight = weight
    self.rel = rel
    self.type = nodeType

  def __str__(self):
    return "name: " + str(self.name) + ", weight: " + str(self.weight) + ", rel: " + str(self.rel) + ", type: " + str(self.type)

class Node:
    def __init__(self, name, postag, nodeType, weight, depth, rootParent):
        self.name = name
        self.postag = postag
        self.nodeType = nodeType
        self.weight = weight
        self.depth = depth
        self.rootParent  = rootParent

    def __str__(self):
        return "name: " + str(self.name) + "\npostag: " + str(self.postag) + ",\nweight: " + str(self.weight) + ",\nnodeType: " + str(self.nodeType)

    def __gt__(self, other):
        return self.weight < other.weight

    def __eq__(self, other):
        return self.weight == other.weight
