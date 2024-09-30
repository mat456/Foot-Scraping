

def map_team(team):
    dict = {
        "Alavés": "Alaves",
        "Almería": "Almeria",
        "Atlético Madrid": "Atletico Madrid",
        "Bayern München": "Bayern Munich",
        "Cádiz": "Cadiz",
        "Brighton & Hove Albion": "Brighton",
        "Darmstadt 98": "Darmstadt",
        "Tottenham Hotspur": "Tottenham",
        "West Ham United": "West Ham",
        "Luton Town": "Luton",
        "Paris Saint-Germain": "Paris",
        "Wolverhampton Wanderers": "Wolves",
        "Hellas Verona": "Verona",
        "Internazionale": "Inter"
    }

    team_good = dict.get(team, team)
    return team_good



