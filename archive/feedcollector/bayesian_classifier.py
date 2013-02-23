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
        return float(self.data[category].get(word, 0) + self.k) / (self.numberOfWordsInCategory(category) + self.k*self.numberOfDistinctWords())
        
    def probabilitiesTextGivenCategory(self, text):
        probabilities = {}
        for category in self.data:
            probability = 1.0
            for word in text:
                probability *= self.probabilityWordGivenCategory(word, category)
            probabilities[category]= probability
            
        return probabilities
        
    def priorProbabilitiesCategories(self):
        numberOfWords = self.numberOfWords()
        numCategories = len(self.data)
        return dict((category, float(self.numberOfWordsInCategory(category) + self.k) / (numberOfWords + self.k*numCategories))
                                    for category in self.data.keys())

    #e.g. categories SPAM and HAM
    #P[SPAM | text] = (P[w_1 | SPAM]*...*P[w_n|SPAM])*P[SPAM] / ((P[w_1|SPAM]*...*P[w_n|SPAM])*P[SPAM] + (P[w_1|HAM]*...*P[w_n|HAM])*P[HAM])
    # where text = w_1 w_2 ... w_n
    def probabilities(self, text):
        words = textprocessing.getWordList(text)
        words = words[0:self.consider_words]
        
        categoryProbabilities = self.priorProbabilitiesCategories()
        textProbabilities = self.probabilitiesTextGivenCategory(words)
        
        totalProbabilityText = 0
        for category, categoryProbability in self.probabilities_categories.items():
            totalProbabilityText += categoryProbability * textProbabilities[category]
        
        if totalProbabilityText == 0: return []
        
        return [(category, float(self.probabilities_categories[category]*textProbabilities[category]) / totalProbabilityText)
                        for category in self.data.keys()]
    
    def load(self, filename):
        filenameDict = "{0}.dict".format(filename)
        filenameWords = "{0}.words".format(filename)
        
        with  open(filenameDict, "r") as fileDict:
            self.data = pickle.load(fileDict)
            
        with open(filenameWords, "r") as fileWords:        
            self.word_count = pickle.load(fileWords)
        
        #directly calculate category probabilities, so that they only need to be calculated once
        self.probabilities_categories = self.priorProbabilitiesCategories()
        
    def save(self, filename):
        filenameDict = "{0}.dict".format(filename)
        filenameWords = "{0}.words".format(filename)
        with open(filenameDict, "w") as fileDict:
            pickle.dump(self.data, fileDict)
            
        with open(filenameWords, "w") as fileWords:
            pickle.dump(self.word_count, fileWords)
        
    def guessCategory(self, text):
        probabilities = self.probabilities(text)
        if probabilities == []:
            return Classifier.UNKNOWN_CATEGORY
        maxProbability = max(probabilities, key=lambda probability: probability[1])
        return maxProbability[0]