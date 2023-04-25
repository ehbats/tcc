import sys, os
sys.path.append(os.path.abspath("."))
from lang_processing.services.get_polarization import GetPolarization

instance = GetPolarization()

polarization = instance.run_with_default_params('HOLD MY BEER. A BUD Light tentou ser cool. O script ofendeu a América. Americanas caiu 80,52% ontem')
print(polarization)

