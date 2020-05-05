class Edge:

  def __init__(self, name, weight, rel, nodeType):
    self.name = name
    self.weight = weight
    self.rel = rel
    self.type = nodeType

  def __str__(self):
    return "name: " + str(self.name) + ", weight: " + str(self.weight) + ", rel: " + str(self.rel) + ", type: " + str(self.type)

class Node:
    def __init__(self, name, postag, edges, weight):
        self.name = name
        self.postag = postag
        self.edges = edges
        self.weight = weight

    def __str__(self):
        return "name: " + str(self.name) + "\npostag: " + str(self.postag) + ",\nweight: " + str(self.weight) + ",\nedges: " + str([str(edge) for edge in self.edges])

    def __cmp__(self, other):
        return self.weight <= other.weight