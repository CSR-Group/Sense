import os 
# from .. import data
import json
import spacy
import nltk

nlp = spacy.load("en_core_web_sm")

# TRAIN_DATASET_PATH = os.path.dirname(os.path.abspath(data.__file__)) + '/commonsenseQA/train.jsonl'
# TEST_DATASET_PATH = os.path.dirname(os.path.abspath(data.__file__)) + '/commonsenseQA/test.jsonl'

TRAIN_DATASET_PATH = "/Users/anushkabaoni/Downloads/Cornell Courses-Spring2020/Advanced AI/CommonsenseQADataset/train_rand_split.jsonl"


def getDataSet(path = None):
    '''   
    Loads the CQA dataset
    Returns: 
    List of Questions
    '''
    questions = []
    if(path == None):
        path = TRAIN_DATASET_PATH
        
    with open(path) as fp:
        for line in fp:
            parsedObject = json.loads(line)
            questions.append(parsedObject)
    return questions


def getSplitDataSet(path = None):
    dataset = getDataSet(path)
    return splitDataSet(dataset)

def splitDataSet(dataset):
    what_questions = []
    where_questions = []
    why_questions = []
    who_questions = []
    which_questions = []
    when_questions = []
    how_questions = []

    rand = []

    for question in dataset:
        assigned = False
        text = set(nltk.word_tokenize(question['question']['stem'].lower()))
        if ("what" in text and "where" not in text and "why" not in text and "who" not in text and "when" not in text and "how" not in text and "which" not in text):
            what_questions.append(question)
            continue
        if ("what" not in text and "where" in text and "why" not in text and "who" not in text and "when" not in text and "how" not in text and "which" not in text):
            where_questions.append(question)
            continue
        if ("what" not in text and "where" not in text and "why" in text and "who" not in text and "when" not in text and "how" not in text and "which" not in text):
            why_questions.append(question)
            continue
        if ("what" not in text and "where" not in text and "why" not in text and "who" in text and "when" not in text and "how" not in text and "which" not in text):
            who_questions.append(question)
            continue
        if ("what" not in text and "where" not in text and "why" not in text and "who" not in text and "when" in text and "how" not in text and "which" not in text):
            when_questions.append(question)
            continue
        if ("what" not in text and "where" not in text and "why" not in text and "who" not in text and "when" not in text and "how" in text and "which" not in text):
            how_questions.append(question)
            continue
        if ("what" not in text and "where" not in text and "why" not in text and "who" not in text and "when" not in text and "how" not in text and "which" in text):
            which_questions.append(question)
            continue
            # whether, whose, whom, how

        doc = nlp(question['question']['stem'].lower())
        for token in doc:
            if (token.dep_ == 'ROOT'):
                childern = [str(child) for child in token.children]
                if ("what" in childern):
                    what_questions.append(question)
                    assigned = True
                    break
                elif ("where" in childern):
                    where_questions.append(question)
                    assigned = True
                    break
                elif ("why" in childern):
                    why_questions.append(question)
                    assigned = True
                    break
                elif ("who" in childern):
                    who_questions.append(question)
                    assigned = True
                    break
                elif ("how" in childern):
                    how_questions.append(question)
                    assigned = True
                    break
                elif ("which" in childern):
                    which_questions.append(question)
                    assigned = True
                    break
                elif ("when" in childern):
                    when_questions.append(question)
                    assigned = True
                    break
        if not assigned:
            rand.append(question)
            for token in doc:
                if ("what" == token.text and 'dobj' == token.dep_):
                    what_questions.append(question)
                    break

    print(len(dataset))
    print("what : ", len(what_questions))
    print("where : ", len(where_questions))
    print("why : ", len(why_questions))
    print("who : ", len(who_questions))
    print("how : ", len(how_questions))
    print("which : ", len(which_questions))
    print("when : ", len(when_questions))
    print(len(what_questions) + len(where_questions) + len(why_questions) + len(who_questions) + len(how_questions) + len( which_questions) + len(when_questions))
    return {"what": what_questions,
            "where": where_questions,
            "why": why_questions,
            "who": who_questions,
            "how": how_questions,
            "which":  which_questions,
            "when": when_questions}
