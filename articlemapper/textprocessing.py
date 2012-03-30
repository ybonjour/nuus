import nltk
import re

def remove_html_tags(data):
    #*? ensures that the next closing bracket is matched
    #and not the last possible closing bracket
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def get_word_list(text):
    text = remove_html_tags(text)
    tokenizer = nltk.tokenize.WordPunctTokenizer()
    words = tokenizer.tokenize(text)
    return words