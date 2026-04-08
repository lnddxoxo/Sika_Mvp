# 30 actions les plus liquides de la BRVM
# Utilisées pour les calculs de score et les scrapers
BRVM30 = {
# SERVICES FINANCIERS
'SGBC': {'nom': 'Societe Generale CI', 'secteur': 'Services financiers'},
'ECOC': {'nom': 'Ecobank CI', 'secteur': 'Services financiers'},
'BOAB': {'nom': 'Bank Of Africa Benin', 'secteur': 'Services financiers'},
'BOABF': {'nom': 'Bank Of Africa Burkina Faso', 'secteur': 'Services financiers'},
'BOAC': {'nom': 'Bank Of Africa CI', 'secteur': 'Services financiers'},
'BOAM': {'nom': 'Bank Of Africa Mali', 'secteur': 'Services financiers'},
'BOAN': {'nom': 'Bank Of Africa Niger', 'secteur': 'Services financiers'},
'BOAS': {'nom': 'Bank Of Africa Senegal', 'secteur': 'Services financiers'},
'BICB': {'nom': 'Banque Internationale Burkina', 'secteur': 'Services financiers'},
'CBIBF': {'nom': 'Coris Bank International', 'secteur': 'Services financiers'},
'STBC': {'nom': 'Standard Chartered Bank CI', 'secteur': 'Services financiers'},
# TELECOMMUNICATIONS
'SNTS': {'nom': 'Sonatel', 'secteur': 'Telecommunications'},
'ORAC': {'nom': 'Orange CI', 'secteur': 'Telecommunications'},
'ONTBF': {'nom': 'Onatel Burkina Faso', 'secteur': 'Telecommunications'},
# ENERGIE
'TTLC': {'nom': 'Total CI', 'secteur': 'Energie'},
'SHEC': {'nom': 'Vivo Energy CI', 'secteur': 'Energie'},
'CIEC': {'nom': 'CIE CI', 'secteur': 'Energie'},
# AGRO-INDUSTRIE
'PALC': {'nom': 'Palm CI', 'secteur': 'Agro-industrie'},
'SPHC': {'nom': 'SAPH CI', 'secteur': 'Agro-industrie'},
'SOGC': {'nom': 'SOGB', 'secteur': 'Agro-industrie'},
'CFAC': {'nom': 'CFAO Motors CI', 'secteur': 'Agro-industrie'},
'SAFC': {'nom': 'SAFCA', 'secteur': 'Agro-industrie'},
# CONSOMMATION DE BASE
'SLBC': {'nom': 'Solibra', 'secteur': 'Consommation de base'},
'SCRC': {'nom': 'Sucrivoire', 'secteur': 'Consommation de base'},
'SDSC': {'nom': 'AGL CI', 'secteur': 'Consommation de base'},
# DISTRIBUTION
'ETIT': {'nom': 'Ecobank Transnational', 'secteur': 'Distribution'},
# TRANSPORT
'ORGT': {'nom': 'Oragroup Togo', 'secteur': 'Transport'},
# INDUSTRIES
'FTSC': {'nom': 'Filtisac CI', 'secteur': 'Industries'},
'UNXC': {'nom': 'Uniwax CI', 'secteur': 'Industries'},
'SIVC': {'nom': 'Erium CI', 'secteur': 'Industries'},
}
BRVM30_TICKERS = list(BRVM30.keys())