import csv
import os 
from .. import data

DATASET_PATH = os.path.dirname(os.path.abspath(data.__file__)) + '/cloze_test_val__winter2018-cloze_test_ALL_val - 1 - 1.csv'

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
