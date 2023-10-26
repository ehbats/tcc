import sys, os
sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath(".."))
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "twittator.settings")
django.setup()
from news_data.models.kaggle_news import KaggleNews
from lang_processing.models.polarity import Polarity
from lang_processing.services.populate_polarization import PopulatePolarity

PopulatePolarity().populate()