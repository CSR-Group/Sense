class Question: 

  def __init__(self):
    self.contexts = []
    self.root = None
    self.questionType = None
    self.candidates = []

  def __str__(self):
    return "root: " + str(self.root) + ",\n contexts: " + str([str(ctx) for ctx in  self.contexts]) + ",\n candidates: " + str(self.candidates) + ", type: " + str(self.questionType)


class Context:
    """Context = Subject Action Object set"""

    def __init__(self):
      self.subjects = []
      self.action = None
      self.objects = []

    def __str__(self):
      return "subjects: " + str([str(sub) for sub  in self.subjects]) + ", action: " + str(self.action) + ", objects: " + str([str(ob) for ob  in self.objects])

class Entity:

  def __init__(self, name, properties):
    self.name = name
    self.properties = {}

  def __str__(self):
    return "name: " + str(self.name) + ", properties: " + str([(k, [str(x) for x in self.properties[k]]) for k in self.properties])


class Subject(Entity):

  def __init__(self, name, properties):
    super().__init__(name,properties)

class Action(Entity):

  def __init__(self, name, properties):
    super().__init__(name,properties)
    

class Object(Entity):

  def __init__(self, name, properties):
    super().__init__(name,properties)
