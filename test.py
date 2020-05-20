from csense.benchmark.cqa import getSplitDataSet
from CommonSenseQA import parseQuestion
from csense.parser.sentence import parse
from csense.mining.conceptnet import search
from concurrent.futures import ThreadPoolExecutor
import threading
import spacy
import nltk

nlp = spacy.load("en_core_web_sm")

def task(rawQuestion, index):
    # print("Executing our Task")
    try:
        outfile = open("outfile_temp.txt", mode="a+")
        count, count1, guessAnswer, guessAnswer1, correctAnswer = scoreCandidates(rawQuestion)
        print(index, " - ", correctAnswer, " - ", guessAnswer, " - " ,guessAnswer1, file=outfile)
        print(index, " - ", correctAnswer, " - ", guessAnswer, " - " ,guessAnswer1)
        if count == 1 or count1 == 1:
            print("#RES:1:",index, file=outfile)
            return 1
        else:
            print("#RES:0:",index, file=outfile)
            return 0
    except Exception as e:
        print(e)
        print(index, ":FAILED")
        print("#RES:F:",index, file=outfile)
        return 0
    finally:
        outfile.close()

def scoreCandidates(rawQuestion):
    
    candidateSetSize = {}
    candidateMap = {}
    candidateMap1 = {}
    question, candidates, correctAnswer = parseQuestion(rawQuestion)
    print(question)
    questionChunks = getChunkSet(question)
    print(questionChunks)
    temp = set()
    questionChunks1 = set()
    for question in questionChunks:
        tempSet = search(question)
        # print(tempSet)
        temp = temp.union(tempSet)
        # print(temp)
    questionChunks1 = questionChunks.union(temp)

    print("questionChunks")
    print(questionChunks)
    for candidate in candidates:
        candidateMap[candidate] = 0
        candidateMap1[candidate] = 0
        candidateChunks = search(candidate.replace(' ','_'))
        candidateChunks.add(candidate)
        candidateChunks.add(candidate.split(' ')[-1])
        # print("candidateChunks: " + candidate)
        # print(candidateChunks)
        candidateSetSize[candidate] = len(candidateChunks)
        for chunk in questionChunks:
            if chunk in candidateChunks:
                candidateMap[candidate] += 1
                
        for chunk in questionChunks1:
            if chunk in candidateChunks:
                candidateMap1[candidate] += 1

    print(candidateMap)
    print(correctAnswer)

    guessAnswer = max(candidateMap, key=candidateMap.get)
    for i in range(len(candidates)):
        if candidateMap[candidates[i]] == candidateMap[guessAnswer] and candidateSetSize[candidates[i]] < candidateSetSize[guessAnswer]:
            guessAnswer = candidates[i]
    print(guessAnswer)
    # if correctAnswer == guessAnswer:
    #     count+=1
    # if candidateMap[correctAnswer] == candidateMap[guessAnswer]:
    #     count1+=1

    guessAnswer1 = max(candidateMap1, key=candidateMap1.get)
    for i in range(len(candidates)):
        if candidateMap1[candidates[i]] == candidateMap1[guessAnswer1] and candidateSetSize[candidates[i]] < candidateSetSize[guessAnswer1]:
            guessAnswer1 = candidates[i]
    print(guessAnswer1)

    if correctAnswer == guessAnswer1 or correctAnswer == guessAnswer:
        count = 1
    else:
        count = 0
    if candidateMap1[correctAnswer] == candidateMap1[guessAnswer1] or candidateMap[correctAnswer] == candidateMap[guessAnswer]:
        count1 = 1
    else:
        count1 = 0
    print("*********")

    return count, count1, guessAnswer, guessAnswer1, correctAnswer
    
def getChunkSet(sentence):
    doc = nlp(sentence)
    p = nltk.PorterStemmer()
    chunks = set()
    for chunk in doc.noun_chunks:
        chunk_without_sw = ""
        for word in chunk.text.lower().split(' '):
            word = ''.join(filter(str.isalnum, word))
            if not word in ['a','the','an']:
                chunks.add(word)
                if chunk_without_sw == "":
                    chunk_without_sw = word
                else:
                    chunk_without_sw = chunk_without_sw + "_" + word
                chunks.add(chunk_without_sw.lower())

        chunks.add(chunk.root.text.lower())
        chunks.add(p.stem(chunk.root.text.lower()))
    return chunks

def main():
    executor = ThreadPoolExecutor(max_workers=10)

    dataset = getSplitDataSet()
    futures = []

    questions = dataset["where"]

    # for index in range(0, len(questions)):
    for index in range(1619,1620):
        res = executor.submit(task, questions[index], index)
        futures.append(res)

    count = 0
    for future in futures:
        count += future.result()

    print(count / len(questions))

if __name__ == '__main__':
    main()
