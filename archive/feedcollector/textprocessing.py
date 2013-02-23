import nltk
import re

def removeHtmlTags(data):
    #*? ensures that the next closing bracket is matched
    #and not the last possible closing bracket
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def getWordList(text):
    text = removeHtmlTags(text)
    tokenizer = nltk.tokenize.WordPunctTokenizer()
    return tokenizer.tokenize(text)
    
def containsLetters(word):
    return re.search("[a-zA-Z]+", word)