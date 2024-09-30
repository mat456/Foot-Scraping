import pandas as pd

annee = "24"

params = pd.read_csv("/Users/mathieulengrand/Desktop/Modele foot/Modèles/Data/params" + annee + ".csv", encoding='utf8')
params = params[["Equipe","Absence 1", "Absence 2", "Absence 3", "Absence 4", "Lien calendrier"]]


mois = {"Janvier": "01", "Février": "02", "Mars": "03", "Avril": "04",
        "Mai": "05", "Juin": "06", "Juillet": "07", "Août": "08",
        "Septembre": "09", "Octobre": "10", "Novembre": "11", "Décembre": "12"}

ligue = {"Premier League": "UK", "Ligue des champions UEFA": "C1","UEFA Champions League": "C1" , "Ligue 1": "FR", "Europa League de l'UEFA": "C3", "UEFA Europa League": "C3", "La Liga" : "ES", "Serie A": "IT", "Fußball-Bundesliga": "AL"}

