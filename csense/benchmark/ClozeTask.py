import csv
import os 
from .. import data

DATASET_PATH = os.path.dirname(os.path.abspath(data.__file__)) + '/cloze_test_val__winter2018-cloze_test_ALL_val - 1 - 1.csv'

class Story:
    """Wrapper for one Story in the Story Cloze Task Dataset"""

    def __init__(self, id, sent1, sent2, sent3, sent4, end1, end2, ans):
        self.id = id
        self.sentence1 = sent1
        self.sentence2 = sent2
        self.sentence3 = sent3
        self.sentence4 = sent4
        self.end1 = end1
        self.end2 = end2
        self.ans = ans

def getDataSet(path = None):
    '''   
    Loads the story cloze dataset
    Returns: 
    List of Stories
    '''
    stories = []
    if(path == None):
        path = DATASET_PATH
    with open(path) as csvfile:
        data = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(data)
        for row in data:
                stories.append(Story(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]))
    return stories
