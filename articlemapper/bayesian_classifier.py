import textprocessing
import pickle

class Classifier:
    def __init__(self, k=1):
        self.data = {}
        self.word_count = {}
        self.k = k #for laplace smoothing
        

    def trainText(self, text, category):
        words = textprocessing.get_word_list(text)
        for word in words:
            self.trainWord(word, category)
        
    def trainWord(self, word, category):
        if not category in self.data:
            self.data[category] = {}
        self.data[category][word] = self.data[category].get(word, 0) + 1
        self.word_count[word] = self.word_count.get(word, 0) + 1

    def numberOfWordsInCategory(self, category):
        return sum(self.data[category].itervalues())
    
    def numberOfWords(self):
        return sum(self.word_count.values())
    
    def numberOfDistinctWords(self):
        return len(self.word_count)

    def probabilityWordGivenCategory(self, word, category):
        return 1.0*(self.data[category].get(word, 0) + self.k) / (self.numberOfWordsInCategory(category) + self.k*self.numberOfDistinctWords())
        
    def probabilitiesTextGivenCategory(self, text):
        probabilities = {}
        for category in self.data:
            probability = 1
            for word in text:
                probability *= self.probabilityWordGivenCategory(word, category)
            probabilities[category]= probability
        return probabilities
        
    def priorProbabilitiesCategories(self):
        probabilities = {}
        for category in self.data:
            probabilities[category] = 1.0*(self.numberOfWordsInCategory(category) + self.k) / (self.numberOfWords() + self.k*len(self.data))
        return probabilities

    #e.g. categories SPAM and HAM
    #P[SPAM | text] = (P[w_1 | SPAM]*...*P[w_n|SPAM])*P[SPAM] / ((P[w_1|SPAM]*...*P[w_n|SPAM])*P[SPAM] + (P[w_1|HAM]*...*P[w_n|HAM])*P[HAM])
    # where text = w_1 w_2 ... w_n
    def probabilities(self, text):
        words = textprocessing.get_word_list(text)
        categoryProbabilities = self.priorProbabilitiesCategories()
        textProbabilities = self.probabilitiesTextGivenCategory(words)
        
        totalProbabilityText = 0
        for category, categoryProbability in categoryProbabilities.items():
            totalProbabilityText += categoryProbability * textProbabilities[category]
        
        probabilities = []
        for category in self.data:
            probability = 1.0*(categoryProbabilities[category]*textProbabilities[category]) / totalProbabilityText
            probabilities.append((category, probability))
        
        return probabilities
    
    def load(self, filename):
        filenameDict = "{0}.dict".format(filename)
        filenameWords = "{0}.words".format(filename)
        fileDict = open(filenameDict, "r")
        fileWords = open(filenameWords, "r")
        self.data = pickle.load(fileDict)
        self.word_count = pickle.load(fileWords)
        
    def save(self, filename):
        filenameDict = "{0}.dict".format(filename)
        filenameWords = "{0}.words".format(filename)
        fileDict = open(filenameDict, "w")
        fileWords = open(filenameWords, "w")
        try:
            pickle.dump(self.data, fileDict)
            pickle.dump(self.word_count, fileWords)
        finally:
            fileDict.close()
            fileWords.close()
        
    def guessCategory(self, text):
        probabilities = self.probabilities(text)
        probabilities.sort(key=lambda probability: probability[1], reverse=True)
        return probabilities[0][0]