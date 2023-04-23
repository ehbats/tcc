import nltk
import spacy
from nltk.corpus import stopwords
from senticnet.senticnet import SenticNet

class GetPolarization:
    def __init__(
            self, 
    ):
        nltk.download('stopwords')
        nltk.download('rslp')
        nltk.download('punkt')

    def text_preprocessing(
            self, 
            text: str,
            lemmatization_lang: str = 'pt',
            lemmatization_size: str = 'lg',
            lang: str = 'portuguese',
    ):
        text = text.lower()
        stopwords = set(stopwords.words(lang))

        add_stopwords = ['em o', '.', '%', ',', 'em este', 'em aquele']
        for stopword in add_stopwords:
            stopwords.add(stopword)

        nlp = spacy.load(f'{lemmatization_lang}_core_news_{lemmatization_size}')
        
        lemmatized_and_tokenized_text = nlp(text)

        lemmatized_tokenized_no_stopwords = [token.lemma_ for token in lemmatized_and_tokenized_text if token.lemma_ not in stopwords]

        return lemmatized_tokenized_no_stopwords

    def get_polatization(
            self,

    ):
        x=1
    def run_with_default_params(
            self,
            text
    ):
        x=1

instance = GetPolarization()
# print(instance.lemmas)