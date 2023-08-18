import sys, os
sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath(".."))
from lang_processing.services.populate_polarization import PopulatePolarity

PopulatePolarity().populate()