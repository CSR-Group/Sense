from csense.parser.context import *
import spacy

nlp = spacy.load("en_core_web_sm")

def getPos(word, doc):
    for token in doc:
        if(token.text == word):
            return token.pos_

## TODO 
# conjuctions of properties 
# conjuctions of dobj
# conjuctions of pobj
# conjuctions of subject

def parse(sentence, questionType, candidates, questionConcept):
    doc = nlp(sentence)
    question = Question()
    question.questionType = questionType
    contextMap = {}
    entityToPropMap = {}
    entityToPrepositionPObjMap = {}
    question.candidates = candidates
    question.questionConcept = questionConcept
    
    # find root 
    for token in doc:
        if(token.dep_ == "ROOT"):
            question.root = token.text
            break

    # associate properties
    for token in doc:
        if token.dep_ == 'amod':
            if token.head.text not in entityToPropMap:
                entityToPropMap[token.head.text] = []
            entityToPropMap[token.head.text].append(str(token.text))
            # { "glass" : ["empty", ..]}
            
    # associate prepositions
    for token in doc:
        if token.dep_ == 'prep':
            if token.head.text not in entityToPrepositionPObjMap:
                entityToPrepositionPObjMap[token.head.text] = []
            entities = []
            for child in token.children:
                if(child.pos_ == "NOUN"):
                    ent = Subject(child.text, {}, child.is_stop)
                if(child.pos_ == "VERB"):
                    ent = Action(child.text, {}, child.is_stop)
                # associate amods of preposition entities. (rent in(prep) glove-shaped(amod) state(ent))
                if(ent.name in entityToPropMap):
                    if("_" not in ent.properties):
                        ent.properties["_"] = []
                    ent.properties["_"].extend(entityToPropMap[ent.name])
                entities.append(ent)
            entityToPrepositionPObjMap[token.head.text].append((token.text,entities))
            # { "rent" : [(in, [state])]}
            #.   (sub) : [(prep, [pobj])]
    
    # find sub - action pairs
    for chunk in doc.noun_chunks:
        if chunk.root.dep_ == 'nsubj':
            sub = Subject(chunk.root.text, {}, chunk.root.is_stop)
            # associating prop with subject
            if(sub.name in entityToPropMap):
                if("_" not in sub.properties):
                    sub.properties["_"] = []
                sub.properties["_"].extend(entityToPropMap[sub.name])
            
            # associating prepositions with subject
            if(sub.name in entityToPrepositionPObjMap):
                for (prep, pobjs) in entityToPrepositionPObjMap[sub.name]:
                    if(prep not in sub.properties):
                        sub.properties[prep] = []
                    sub.properties[prep].extend(pobjs)
            
            # finding verb
            if(getPos(chunk.root.head.text, doc) == 'VERB'):
                verb = Action(chunk.root.head.text, {}, chunk.root.head.is_stop)
                
                # associating prop with dobject
                if(verb.name in entityToPropMap):
                    if("_" not in verb.properties):
                        verb.properties["_"] = []
                    verb.properties["_"].extend(entityToPropMap[verb.name])

                # associating prepositions with subject
                if(verb.name in entityToPrepositionPObjMap):
                    for (prep, pobjs) in entityToPrepositionPObjMap[verb.name]:
                        if(prep not in verb.properties):
                            verb.properties[prep] = []
                        verb.properties[prep].extend(pobjs)
                
                
                
                context = Context()
                context.action = verb
                context.subjects.append(sub)
                #todo handle conjunction of subjects
                contextMap[verb.name] = context


    for chunk in doc.noun_chunks:
        # associate dobjs
        if chunk.root.dep_ == 'dobj':
            obj = Object(chunk.root.text, {}, chunk.root.is_stop)
            # associating prop with dobject
            if(obj.name in entityToPropMap):
                if("_" not in obj.properties):
                    obj.properties["_"] = []
                obj.properties["_"].extend(entityToPropMap[obj.name])

            # associating prepositions with subject
            if(obj.name in entityToPrepositionPObjMap):
                for (prep, pobjs) in entityToPrepositionPObjMap[obj.name]:
                    if(prep not in obj.properties):
                        obj.properties[prep] = []
                    obj.properties[prep].extend(pobjs)
                    
            if(getPos(chunk.root.head.text, doc) == 'VERB'):
                verb = chunk.root.head.text
                if(verb in contextMap):
                    contextMap[verb].objects.append(obj)

            
    for key in contextMap:
        question.contexts.append(contextMap[key])
    
    return question