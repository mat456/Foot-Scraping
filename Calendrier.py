import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
from Param import params
from selenium import webdriver
import os

def calendar(team):

    equipe = params[params.Equipe == team]
    URL = equipe["Lien calendrier"].tolist()[0]
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")


    tab = soup.find('table', attrs={"id": "matchlogs_for"}).find_all("tr")
    journees = []
    for elt in range(1, len(tab)):
        qualif = tab[elt].find_all('td',attrs={"class": "left"})[1].find_all('a')[0].get_text()
        if (not tab[elt].find_all('td', attrs={"class": "left group_start"})) or (tab[elt].find_all('td', attrs={"class": "left group_start"})[0].find('a') is None) or ("Rapport" not in tab[elt].find_all('td', attrs={"class": "left group_start"})[0].find('a').get_text()) or (re.search(" tour de qualification", qualif) is not None) \
                or (re.search("barrage", qualif) is not None) or (re.search("qualifying", qualif) is not None) or (re.search("Play-off", qualif) is not None):
            continue
        else:
            link = tab[elt].find_all('td', attrs={"class": "left group_start"})[0].find('a').get('href')
            link = "https://fbref.com" + link
            compet = tab[elt].find_all('td', attrs={"class": "left"})[0].find_all('a')[0].get_text()
            match = tab[elt].find_all('td', attrs={"class": "left"})[1].find_all('a')[0].get_text()
            journee={}
            journee["Match"] = match
            journee["Compet"] = compet
            journee["Lien"] = link
            journees.append(journee)

    list_compet = ['Premier League', 'Ligue 1', 'Champions Lg', 'Europa Lg', 'La Liga', 'Serie A', 'Bundesliga']
    calendar = pd.DataFrame(journees)
    calendar = calendar[calendar["Compet"].isin(list_compet)]
    return calendar

