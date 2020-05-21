from csense.parser.sentence import parse
from csense.mining.search import HeuristicSearch
from csense.mining.search import RelatednessSearch
from csense.mining.conceptnet import lookup
from csense.benchmark.cqa import getSplitDataSet

from concurrent.futures import ThreadPoolExecutor
import threading
import random

def parseQuestion(question):
    candidates = []
    answer = None
    answerLabel = question['answerKey']
    for choice in question['question']['choices']:
        candidates.append(choice['text'])
        if(choice['label'] == answerLabel):
            answer = choice['text']
    return (question['question']['stem'], candidates, answer)

def task(rawQuestion, index):
    question, candidate, correctAnswer = parseQuestion(rawQuestion)
    parsedSentence = parse(question, "WHERE", candidate)
    print(parsedSentence)


dataset = getSplitDataSet()
questions = dataset["where"]

print(questions[7])
task(questions[7],7)
# for index in range(0, len(questions)):
#     res = executor.submit(task, questions[index], index)
#     futures.append(res)