from csense.parser.sentence import parse
from csense.mining.search import HeuristicSearch


sentence = "If you have a empty glass and are thirsty, where would you put the glass?"
parsedSentence = parse(sentence, "WHERE",["refrigerator", "table", "dishwasher", "water cooler", "dining room"], "glass")
print(parsedSentence)

search = HeuristicSearch(parsedSentence)
search.run(2)
