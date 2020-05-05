class Question: 

  def __init__(self):
    self.contexts = []
    self.root = None
    self.questionType = None
    self.candidates = []

  def __str__(self):
    return "root: " + str(self.root) + ",\n contexts: " + str([str(ctx) for ctx in  self.contexts]) + ",\n candidates: " + str(self.candidates) + ",\n type: " + str(self.questionType)

class Context:
    """Context = Subject Action Object set"""

    def __init__(self):
      self.subjects = []
      self.action = None
      self.objects = []

    def __str__(self):
      return "subjects: " + str([str(sub) for sub  in self.subjects]) + ",action: " + str(self.action) + ",objects: " + str([str(ob) for ob  in self.objects])

class Entity:

  def __init__(self, name, properties, is_stop_word):
    self.name = name
    self.properties = {}
    self.is_stop_word = is_stop_word

  def __str__(self):
    return "name: " + str(self.name) + ", properties: " + str([(k, [str(x) for x in self.properties[k]]) for k in self.properties])


class Subject(Entity):

  def __init__(self, name, properties, is_stop_word):
    super().__init__(name,properties, is_stop_word)

class Action(Entity):

  def __init__(self, name, properties, is_stop_word):
    super().__init__(name,properties, is_stop_word)
    

class Object(Entity):

  def __init__(self, name, properties, is_stop_word):
    super().__init__(name,properties, is_stop_word)
