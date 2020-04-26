import os 
from .. import data
import json

TRAIN_DATASET_PATH = os.path.dirname(os.path.abspath(data.__file__)) + '/commonsenseQA/train.jsonl'
TEST_DATASET_PATH = os.path.dirname(os.path.abspath(data.__file__)) + '/commonsenseQA/test.jsonl'


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

