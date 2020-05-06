from csense.parser.sentence import parse
from csense.mining.search import HeuristicSearch
from csense.mining.conceptnet import lookup
from csense.benchmark.cqa import getSplitDataSet

def parseQuestion(question):
    candidates = []
    answer = None
    answerLabel = question['answerKey']
    for choice in question['question']['choices']:
        candidates.append(choice['text'])
        if(choice['label'] == answerLabel):
            answer = choice['text']
    return (question['question']['stem'], candidates, answer)

dataset = getSplitDataSet()
whereQuestions = dataset["where"][0:100]
count = 0

for index in range(37,len(whereQuestions)):
    question, candidate, correctAnswer = parseQuestion(whereQuestions[index])
    # print(question, candidate, correctAnswer)
    parsedSentence = parse(question, "WHERE", candidate)
    search = HeuristicSearch(parsedSentence)
    answer = search.run()

    print(index, " -", correctAnswer, " - ", answer)
    if correctAnswer == answer:
        count+=1
    print(count/(index+1))
    break


print(count)
