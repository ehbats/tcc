import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import RSLPStemmer

class GetPolarization:
    def __init__(self, lang: str = 'portuguese'):
        nltk.download('snowball_data')
        nltk.download('stopwords')
        nltk.download('rslp')
        self.stopwords = set(stopwords.words(lang))
        
        self.rslp = RSLPStemmer()
        

instance = GetPolarization()
