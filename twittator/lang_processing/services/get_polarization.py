import spacy
import nltk
from nltk.corpus import stopwords
from senticnet.babelsenticnet import BabelSenticNet
from senticnet.senticnet import SenticNet

class GetPolarization:
    def __init__(
            self, 
    ):
        # IF NLTK RETURNS AN ERROR, UNCOMMENT THESE LINES
        # nltk.download('stopwords')
        # nltk.download('rslp')
        # nltk.download('punkt')
        pass

    def text_preprocessing(
            self, 
            text: str,
            lemmatization_lang: str = 'pt',
            lemmatization_size: str = 'lg',
            lang: str = 'portuguese',
    ):
        text = text.lower()

        stopwords_set = set(stopwords.words(lang))
        stop_words_english = set(stopwords.words('english'))

        add_stopwords = ['em o', '.', '%', ',', 'em este', 'em aquele']
        for stopword in add_stopwords:
            stopwords_set.add(stopword)

        nlp = spacy.load(f'{lemmatization_lang}_core_news_{lemmatization_size}')
        
        lemmatized_and_tokenized_text = nlp(text)

        lemmatized_tokenized_no_stopwords = [token.lemma_ for token in lemmatized_and_tokenized_text if token.lemma_ not in stopwords_set]
        lemma_token_no_stop_include_english = [token for token in lemmatized_tokenized_no_stopwords if token not in stop_words_english]

        return lemma_token_no_stop_include_english

    def get_mean_polarity(
            self,
            tokens: list,
            lang: str = 'pt'
    ):
        bsn = BabelSenticNet(lang)
        backup_polarity = SenticNet()
        token_amount = len(tokens)
        polarity_list = []
        word_list = []
        for token in tokens:
            failed_polarity = False
            try:
                polarity_list.append(bsn.polarity_value(token))
            except:
                failed_polarity = True
                print(f'COULD NOT LOAD POLARITY FOR TOKEN {token} IN {lang} LANGUAGE! WILL ATTEMPT WITH WHOLE SENTICNET')
            if failed_polarity:
                try:
                    polarity_list.append(backup_polarity.polarity_value(token))
                except:
                    failed_final = True
                    print(f'COULD NOT LOAD POLARITY FOR TOKEN {token} WITH BACKUP POLARITY!')
                
        polarity_list = [float(polarity) if type(polarity) == str else polarity for polarity in polarity_list]

        mean_polarity = sum(polarity_list) / token_amount

        return mean_polarity

    def run_with_default_params(
            self,
            text: str
    ):
        lemmatized_tokenized_no_stopwords = self.text_preprocessing(text)
        polarization = self.get_mean_polarity(lemmatized_tokenized_no_stopwords)

        return polarization
