import textprocessing
import pickle

class Classifier:
    UNKNOWN_CATEGORY = "Unknown"
    def __init__(self, k=1, consider_words=10):
        self.data = {}
        self.word_count = {}
        self.probabilities_categories = {}
        self.k = k #for laplace smoothing
        self.consider_words = consider_words

    def trainText(self, text, category):
        words = textprocessing.getWordList(text)
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
            probability = 1.0
            first = True
            idx = 0
            for word in text:
                probability = probability * self.probabilityWordGivenCategory(word, category)
                idx += 1
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
        print text[0:100].encode('latin1', 'ignore')
        words = textprocessing.getWordList(text)
        words = words[0:self.consider_words]
        
        categoryProbabilities = self.priorProbabilitiesCategories()
        #print self.probabilities_categories
        textProbabilities = self.probabilitiesTextGivenCategory(words)
        print textProbabilities
        
        totalProbabilityText = 0
        for category, categoryProbability in self.probabilities_categories.items():
            totalProbabilityText += categoryProbability * textProbabilities[category]
        
        if totalProbabilityText == 0:
            return []
        
        probabilities = []
        for category in self.data:
            probability = 1.0*(self.probabilities_categories[category]*textProbabilities[category]) / totalProbabilityText
            probabilities.append((category, probability))
        
        print probabilities
        return probabilities
    
    def load(self, filename):
        filenameDict = "{0}.dict".format(filename)
        filenameWords = "{0}.words".format(filename)
        fileDict = open(filenameDict, "r")
        fileWords = open(filenameWords, "r")
        self.data = pickle.load(fileDict)
        self.word_count = pickle.load(fileWords)
        #directly calculate category probabilities, so that they only need to be calculated once
        self.probabilities_categories = self.priorProbabilitiesCategories()
        
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
        if probabilities == []:
            return Classifier.UNKNOWN_CATEGORY
        probabilities.sort(key=lambda probability: probability[1], reverse=True)
        return probabilities[0][0]