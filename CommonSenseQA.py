from csense.parser.sentence import parse
from csense.mining.search import HeuristicSearch
from csense.mining.conceptnet import lookup
from csense.benchmark.cqa import getSplitDataSet
import traceback

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
    # print("Executing our Task")
    try:
        outfile = open("outfile_SA1_where.txt", mode="a+")
        question, candidate, correctAnswer = parseQuestion(rawQuestion)
        parsedSentence = parse(question, "WHERE", candidate)
        search = HeuristicSearch(parsedSentence)
        answer = search.run()

        print(index, " - ", correctAnswer, " - ", answer, file=outfile)
        print(index, " - ", correctAnswer, " - ", answer)
        if correctAnswer == answer:
            print("#RES:1:",index, file=outfile)
            return 1
        else:
            print("#RES:0:",index, file=outfile)
            return 0
    except Exception as e:
        track = traceback.format_exc()
        print(track)
        print(e)
        print(index, ":FAILED")
        print("#RES:F:",index, file=outfile)
        return 0
    finally:
        outfile.close()

def main():
    executor = ThreadPoolExecutor(max_workers=1)

    dataset = getSplitDataSet()
    futures = []

    questions = dataset["where"]

    for index in range(0, len(questions)):
        res = executor.submit(task, questions[index], index)
        futures.append(res)

    count = 0
    for future in futures:
        count += future.result()

    print(count / len(questions))

if __name__ == '__main__':
    main()

# def parseQuestion(question):
#     candidates = []
#     answer = None
#     answerLabel = question['answerKey']
#     for choice in question['question']['choices']:
#         candidates.append(choice['text'])
#         if(choice['label'] == answerLabel):
#             answer = choice['text']
#     return (question['question']['stem'], candidates, answer)
#
# dataset = getSplitDataSet()
# whereQuestions = dataset["where"][0:100]
# count = 0
#
# for index in range(37,len(whereQuestions)):
#     question, candidate, correctAnswer = parseQuestion(whereQuestions[index])
#     # print(question, candidate, correctAnswer)
#     parsedSentence = parse(question, "WHERE", candidate)
#     search = HeuristicSearch(parsedSentence)
#     answer = search.run()
#
#     print(index, " -", correctAnswer, " - ", answer)
#     if correctAnswer == answer:
#         count+=1
#     print(count/(index+1))
#     break
#
#
# print(count)
