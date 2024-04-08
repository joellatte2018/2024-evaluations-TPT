# < PREDICTION DE LA TEMPERATURE A ABIDJAN >

J'utilise des données météo historiques qui peuvent être récupérées avec Historical Weather 
API (Open-Meteo).  Cette API est basée sur des ensembles de données de réanalyse des observations 
provenant de différentes sources (stations météorologiques, radars, satellites, etc.) et, grâce à des 
modèles mathématiques, fournit des informations météorologiques historiques détaillées pour une 
très grande variété des endroits dont ceux qui n'avaient pas de stations météorologiques à proximité.
Je récupére une série temporelle de température à 2m du sol (« Temperature (2 m) ») pour 
la ville d'Abidjan afin de faire une prediction de la teperature  pour une journée avec 
un pas de temps de 3h : 00h, 03h, 06h, …, 21h.

# Data flow & architecture
 -architecture de l'application:

 _entrée:une date
 _pretraitement effectuées sur la date
 _couche du modele:modele SARIMAX(4,1,5)
 _sortie:prediction de la temperature

 -Data flow
 _collecte des données à partir de historical wheather API,les données vont du 01-01-2020 AU 31-12-2023
 _pretraitement effectués 
 _entraitenement du modele
 _optimisation des hyperparametres
 _evaluation du modele



# Main technologies used and for which purpose
STATMODELS for using statictics model
FASTAPI for making API
UVICORN for running API server
SQLITE for saving data into database
pydantic for making control on input data



# Running locally
Instructions to install dependencies, run, build, test

# CI/CD steps
Short description of each step with their outputs (if any)
