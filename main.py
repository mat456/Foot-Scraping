# A chaque nouvelle saison, changer année dans param


from Calendrier import calendar
from Foot import scrap_match

uk = ["Tottenham", "Aston Villa", "Brighton", "Arsenal", "West Ham", "Sheffield United", "Burnley", "Newcastle United",
      "Manchester City", "Manchester United", "Chelsea", "Crystal Palace", "Luton", "Wolves", "Liverpool", "Fulham",
      "Everton", "Nottingham Forest", "Brentford", "Bournemouth"]

es = ["Real Sociedad", "Sevilla", "Osasuna", "Athletic Club", "Atletico Madrid", "Girona", "Barcelona", "Almeria",
      "Alaves", "Villarreal", "Cadiz", "Granada", "Celta Vigo", "Mallorca", "Las Palmas", "Real Betis", "Getafe",
      "Real Madrid", "Rayo Vallecano", "Valencia"]

it = ["Inter", "Lazio", "Atalanta", "Roma", "Sassuolo", "Cagliari", "Fiorentina", "Genoa", "Milan", "Bologna",
      "Frosinone", "Udinese", "Verona", "Napoli", "Lecce", "Monza", "Juventus", "Torino", "Salernitana", "Empoli"]

fr = ["Paris", "Nice", "Lens", "Marseille", "Lyon", "Monaco", "Rennes", "Metz", "Nantes", "Lorient", "Lille",
      "Strasbourg", "Montpellier", "Clermont Foot", "Le Havre", "Reims", "Toulouse", "Brest"]

al = ["Bayern Munich", "Dortmund", "Freiburg", "Bayer Leverkusen", "Mainz 05", "Union Berlin", "Wolfsburg",
      "RB Leipzig", "Hoffenheim", "Mönchengladbach", "Köln", "Stuttgart", "Heidenheim", "Eintracht Frankfurt",
      "Augsburg", "Werder Bremen", "Bochum", "Darmstadt"]

end = ["Bournemouth", "Almeria", "Lecce"]

for team in end:
    calendrier = calendar(team).Lien
    print(scrap_match(team, calendrier))
