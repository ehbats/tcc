import spacy
import nltk
from nltk.corpus import stopwords
from senticnet.babelsenticnet import BabelSenticNet
from senticnet.senticnet import SenticNet

class GetPolarization:
    def __init__(
            self,
            stopwords_lang: str = 'portuguese',
            lemmatization_lang: str = 'pt',
            lemmatization_size: str = 'lg',
            sentic_lang: str = 'pt'
    ):
        """
        This constructor method initiates the necessary data fetched from spacy, SenticNet and nltk.
        Doing this on the constructor method avoids reloading the data every time a method is ran,
        thus reducing process time. Note that it receives as params configurations that are useful
        for the algorithm. The user may want to reduce the lemmatization size to greatly reduce the 
        process time, as the 'lg' lemmatization set takes a long time to load.
        """
        # IF NLTK RETURNS AN ERROR, UNCOMMENT THESE LINES
        # nltk.download('stopwords')
        # nltk.download('rslp')
        # nltk.download('punkt')
        self.stopwords_set = set(stopwords.words(stopwords_lang))
        self.stopwords_english = set(stopwords.words('english'))
        self.nlp = spacy.load(f'{lemmatization_lang}_core_news_{lemmatization_size}')
        self.sentic = BabelSenticNet(sentic_lang)
        self.full_sentic = SenticNet()

    def text_preprocessing(
            self, 
            text: str,
    ):
        """
        Preprocesses the text to make it suitable for analysis and to calculate polarization.
        This lower cases the text, lemmatizes it using spacy's lemmatization tool, and then
        removes the stopwords from the text.
        """
        text = text.lower()

        stopwords_set = self.stopwords_set
        stop_words_english = self.stopwords_english

        add_stopwords = [
            'em o', 
            '.', 
            '%', 
            ',', 
            'em este', 
            'em aquele', 
            'em este', 
            'de o', 
            'mme', 
            'por o', 
            ')', 
            '(', 
            'a o',
            'por o',
            'de este',
            'de isso',
            'de aquele',
            ';',
            ':',
            '"',
            '?',
            '“',
            '”',
            "'",
            '-',
            "):"
            ]
        for stopword in add_stopwords:
            stopwords_set.add(stopword)

        nlp = self.nlp
        
        lemmatized_and_tokenized_text = nlp(text)
        # TODO: evaluate if it would be better to remove the stopwords BEFORE the lemmatization
        lemmatized_tokenized_no_stopwords = [token.lemma_ for token in lemmatized_and_tokenized_text if token.lemma_ not in stopwords_set]
        lemma_token_no_stop_include_english = [token for token in lemmatized_tokenized_no_stopwords if token not in stop_words_english]

        return lemma_token_no_stop_include_english

    def get_mean_polarity(
            self,
            tokens: list,
            lang: str = 'pt'
    ):
        """
        Receives a list of tokens, generates a polarization list from these tokens and the polarization mean. Returns both the list and the mean 
        """
        bsn = self.sentic
        backup_polarity = self.full_sentic
        token_amount = len(tokens)
        polarity_list = []
        sentic_polarization_list = []
        for token in tokens:
            failed_polarity = False
            try:
                polarity_list.append(bsn.polarity_value(token))
                sentics = bsn.sentics(token)
                sentic_polarization = (sentics['pleasantness'] + abs(sentics['attention']) - abs(sentics['sensitivity']) + sentics['aptitude']) / 3
                sentic_polarization_list.append(sentic_polarization)
            except:
                failed_polarity = True
            if failed_polarity:
                try:
                    polarity_list.append(backup_polarity.polarity_value(token))
                except:
                    pass
                
        polarity_list = [float(polarity) if type(polarity) == str else polarity for polarity in polarity_list]

        mean_polarity = sum(polarity_list) / token_amount

        return (mean_polarity, polarity_list, sentic_polarization_list)

    def run_with_default_params(
            self,
            text: str
    ):
        """
        Articulates this class's methods to generate the polarization with the default params created.
        Returns the words considered relevant (no stopwords and tokenized), the mean polarization
        and the list of the calculated polarities.
        """
        lemmatized_tokenized_no_stopwords = self.text_preprocessing(text)
        polarization, polarity_list, sentic_polarization_list = self.get_mean_polarity(lemmatized_tokenized_no_stopwords)

        return lemmatized_tokenized_no_stopwords, polarization, polarity_list, sentic_polarization_list
