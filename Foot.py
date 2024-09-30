import requests
from bs4 import BeautifulSoup
from sele import recup_onglets
import re
import time
from Param import params, mois, ligue
import unidecode
import pandas as pd
import datetime
from mapping_team import map_team
from selenium import webdriver
import os


def scrap_match(team, calendrier):
    matchs = []
    for url in calendrier:
        match = {}
        page = requests.get(url)
        time.sleep(6)
        soup = BeautifulSoup(page.content, "html.parser")

        # Verification Match annulé
        cancel = False
        box = soup.find_all('div', class_='scorebox_meta')
        div = box[0].find_all('div')
        for elt in div:
            test = re.findall("annulé", elt.get_text())
            test2 = re.findall("accordé", elt.get_text())
            test3 = re.findall("suspendu", elt.get_text())
            if (len(test) + len(test2) + len(test3)) > 0:
                cancel = True

        if cancel == True:
            continue

        # Team
        box = soup.find_all('div', class_='scorebox')
        equipe = box[0].find_all('a')[0].get_text()
        equipe = map_team(equipe)

        # Ligue
        box = soup.find_all('div', attrs={"id": "content"})[0].find_all("a")
        champ = ligue[box[0].get_text()]

        # Adversaire
        box = soup.find_all('strong')[5].get_text().strip()
        box2 = soup.find_all('strong')[6].get_text().strip()
        if len(re.findall("Capitaine", box)) > 0:
            adv = box2
        else:
            adv = box

        adv = map_team(adv)

        # Date
        box = soup.find_all('div', class_='scorebox_meta')
        date_game = box[0].find_all('a')[0].get_text()
        date_game = date_game.split(' ', 4)[1] + "/" + mois[date_game.split(' ', 4)[2]] + "/" + date_game.split(' ', 4)[
            3]

        date_fmt = datetime.date(int(date_game.split('/')[2]), int(date_game.split('/')[1]),
                                 int(date_game.split('/')[0]))
        if date_fmt > datetime.date.today():
            break

        # GOALS
        score = soup.find_all('div', class_='score')
        g1 = score[0].get_text()
        g2 = score[1].get_text()

        # XG
        xg = soup.find_all('div', attrs={"class": "score_xg"})
        xg1 = float(xg[0].get_text().replace(",", "."))
        xg2 = float(xg[1].get_text().replace(",", "."))

        # PSXG
        exp = soup.body.findAll('table')
        id_goal = re.findall(r"keeper_stats_\w*", str(exp))
        psxg = soup.find_all('table', attrs={"id": id_goal[0]})[0].find_all("tr")
        psxg1 = psxg[len(psxg) - 1].find_all('td', attrs={"class": "right"})[5].get_text()
        psxg = soup.find_all('table', attrs={"id": id_goal[1]})[0].find_all("tr")
        psxg2 = psxg[len(psxg) - 1].find_all('td', attrs={"class": "right"})[5].get_text()

        # XA - code obsolete car recuperation dans l'onglet passes (via selenium)
        # exp = soup.body.findAll('table')
        # id_name = re.findall(r"stats_\S*_summary", str(exp))
        # xa = soup.find_all('table', attrs={"id": id_name[0]})[0].find_all("tr")
        # xa1 = xa[len(xa)-1].find_all('td', attrs={"class": "right"})[16].get_text()
        # xa = soup.find_all('table', attrs={"id": id_name[1]})[0].find_all("tr")
        # xa2 = xa[len(xa)-1].find_all('td', attrs={"class": "right"})[16].get_text()

        # AMT
        exp = soup.body.findAll('table')
        id_name = re.findall(r"stats_\S*_summary", str(exp))
        amt = soup.find_all('table', attrs={"id": id_name[0]})[0].find_all("tr")
        amt1 = amt[len(amt) - 1].find_all('td', attrs={"class": "right"})[17].get_text()
        amt = soup.find_all('table', attrs={"id": id_name[1]})[0].find_all("tr")
        amt2 = amt[len(amt) - 1].find_all('td', attrs={"class": "right"})[17].get_text()

        # Tcl et Int
        exp = soup.body.findAll('table')
        id_name = re.findall(r"stats_\S*_summary", str(exp))
        tcl = soup.find_all('table', attrs={"id": id_name[0]})[0].find_all("tr")
        tcl1 = int(tcl[len(tcl) - 1].find_all('td', attrs={"class": "right"})[11].get_text()) + int(
            tcl[len(tcl) - 1].find_all('td', attrs={"class": "right"})[12].get_text())
        tcl = soup.find_all('table', attrs={"id": id_name[1]})[0].find_all("tr")
        tcl2 = int(tcl[len(tcl) - 1].find_all('td', attrs={"class": "right"})[11].get_text()) + int(
            tcl[len(tcl) - 1].find_all('td', attrs={"class": "right"})[12].get_text())

        # Dribbles
        exp = soup.body.findAll('table')
        id_name = re.findall(r"stats_\S*_summary", str(exp))

        drr = soup.find_all('table', attrs={"id": id_name[0]})[0].find_all("tr")
        drr1 = drr[len(drr) - 1].find_all('td', attrs={"class": "right"})[25].get_text()
        drr = soup.find_all('table', attrs={"id": id_name[1]})[0].find_all("tr")
        drr2 = drr[len(drr) - 1].find_all('td', attrs={"class": "right"})[25].get_text()

        drt = soup.find_all('table', attrs={"id": id_name[0]})[0].find_all("tr")
        drt1 = drt[len(drt) - 1].find_all('td', attrs={"class": "right"})[26].get_text()
        drt = soup.find_all('table', attrs={"id": id_name[1]})[0].find_all("tr")
        drt2 = drt[len(drt) - 1].find_all('td', attrs={"class": "right"})[26].get_text()

        # Progressive possession et passes
        exp = soup.body.findAll('table')
        id_name = re.findall(r"stats_\S*_summary", str(exp))

        prog_pass = soup.find_all('table', attrs={"id": id_name[0]})[0].find_all("tr")
        prog_pass1 = prog_pass[len(prog_pass) - 1].find_all('td', attrs={"class": "right"})[22].get_text()
        prog_pass = soup.find_all('table', attrs={"id": id_name[1]})[0].find_all("tr")
        prog_pass2 = prog_pass[len(prog_pass) - 1].find_all('td', attrs={"class": "right"})[22].get_text()

        prog_drib = soup.find_all('table', attrs={"id": id_name[0]})[0].find_all("tr")
        prog_drib1 = prog_drib[len(prog_drib) - 1].find_all('td', attrs={"class": "right"})[24].get_text()
        prog_drib = soup.find_all('table', attrs={"id": id_name[1]})[0].find_all("tr")
        prog_drib2 = prog_drib[len(prog_drib) - 1].find_all('td', attrs={"class": "right"})[24].get_text()

        # Passing surface , possession surface , erreur, duels aeriens

        stats = recup_onglets(url)
        passe_surface1 = stats[0]
        passe_surface2 = stats[1]
        poss_surface1 = stats[2]
        poss_surface2 = stats[3]
        xa1 = stats[4]
        xa2 = stats[5]
        erreur1 = stats[6]
        erreur2 = stats[7]
        aerien1 = stats[8]
        aerien2 = stats[9]
        xg1_dead = stats[10]
        g1_dead = stats[11]
        xg2_dead = stats[12]
        g2_dead = stats[13]

        # Card

        eventa = soup.find_all('div', class_='event')[0].find_all('div')
        eventb = soup.find_all('div', class_='event')[1].find_all('div')

        card_A = 0
        for elt in eventa:
            if elt.find_all('div', class_="event_icon red_card") or elt.find_all('div',
                                                                                 class_="event_icon yellow_red_card"):
                card = elt.get_text()[-4:]
                card_A = int(re.findall(r"\d?\d", card)[0])
                break

        card_B = 0
        for elt in eventb:
            if elt.find_all('div', class_="event_icon red_card") or elt.find_all('div',
                                                                                 class_="event_icon yellow_red_card"):
                card = elt.get_text()[-4:]
                card_B = int(re.findall(r"\d?\d", card)[0])
                break

        if card_A > 0 and card_A < 80:
            red_card_team = "O"
        else:
            red_card_team = None

        if card_B > 0 and card_B < 80:
            red_card_adv = "O"
        else:
            red_card_adv = None

        # First Goal

        first_goala = 100
        for elt in eventa:
            if elt.find_all('div', class_='event_icon goal'):
                goal = elt.get_text()[-5:]
                first_goala = int(re.findall(r"\d?\d", goal)[0])
                break

        first_goalb = 100
        for elt in eventb:
            if elt.find_all('div', class_='event_icon goal'):
                goal = elt.get_text()[-5:]
                first_goalb = int(re.findall(r"\d?\d", goal)[0])
                break

        if first_goala < first_goalb:
            first_score = equipe
        elif first_goala > first_goalb:
            first_score = adv
        else:
            first_score = None

        # Liste des joueurs
        exp = soup.body.findAll('table')
        id_name = re.findall(r"stats_\S*_summary", str(exp))
        it1 = soup.find_all('table', attrs={"id": id_name[0]})[0].find_all("tr")
        it2 = soup.find_all('table', attrs={"id": id_name[1]})[0].find_all("tr")

        listeA = []
        for elt in range(2, len(it1) - 1):
            player = {}
            try:
                name = unidecode.unidecode(it1[elt].find_all("a")[0].get_text().upper())
            except:
                continue
            if len(it1[elt].find_all("td")[4]) > 0:
                temps = int(it1[elt].find_all("td")[4].get_text())
            else:
                temps = 0
            if temps > 20:
                listeA.append(name)

        listeB = []
        for elt in range(2, len(it2) - 1):
            player = {}
            try:
                name = unidecode.unidecode(it2[elt].find_all("a")[0].get_text().upper())
            except:
                continue
            if len(it2[elt].find_all("td")[4]) > 0:
                temps = int(it2[elt].find_all("td")[4].get_text())
            else:
                temps = 0
            if temps > 20:
                listeB.append(name)

        # Inversement des stats si extérieur

        lieu = "H"


        if adv == team:
            adv = equipe
            equipe = team
            lieu = "A"
            temp = g1
            g1 = g2
            g2 = temp
            temp = xg1
            xg1 = xg2
            xg2 = temp
            temp = psxg1
            psxg1 = psxg2
            psxg2 = temp
            temp = xa1
            xa1 = xa2
            xa2 = temp
            temp = amt1
            amt1 = amt2
            amt2 = temp
            temp = tcl1
            tcl1 = tcl2
            tcl2 = temp
            temp = erreur1
            erreur1 = erreur2
            erreur2 = temp
            temp = drr1
            drr1 = drr2
            drr2 = temp
            temp = drt1
            drt1 = drt2
            drt2 = temp
            temp = passe_surface1
            passe_surface1 = passe_surface2
            passe_surface2 = temp
            temp = aerien1
            aerien1 = aerien2
            aerien2 = temp
            temp = xg1_dead
            xg1_dead = xg2_dead
            xg2_dead = temp
            temp = g1_dead
            g1_dead = g2_dead
            g2_dead = temp
            temp = poss_surface1
            poss_surface1 = poss_surface2
            poss_surface2 = temp
            temp = prog_pass1
            prog_pass1 = prog_pass2
            prog_pass2 = temp
            temp = prog_drib1
            prog_drib1 = prog_drib2
            prog_drib2 = temp
            temp = red_card_team
            red_card_team = red_card_adv
            red_card_adv = temp
            temp = listeA
            listeA = listeB
            listeB = listeA

        # Noter s'il y a eu expulsion durant le match

        if red_card_adv == 'O':
            red_card = "Rouge 2"
        elif red_card_team == 'O':
            red_card = "Rouge 1"
        else:
            red_card = None

        if g1 > g2:
            res = "V"
        elif g1 < g2:
            res = "D"
        else:
            res = "N"

        # Noter si l'équipe a su garder ou revenir au score

        if (first_score == team) and (res == "V"):
            garde_score = "O"
        elif (first_score == team) and (res != "V"):
            garde_score = "N"
        else:
            garde_score = None

        if (first_score == adv) and (res != "D"):
            retour_score = "O"
        elif (first_score == adv) and (res == "D"):
            retour_score = "N"
        else:
            retour_score = None

        # Vérifier la présence ou non des joueurs clés

        key1 = params[params.Equipe == team]["Absence 1"].tolist()[0].upper().split("/")
        key2 = params[params.Equipe == team]["Absence 2"].tolist()[0].upper().split("/")
        key3 = params[params.Equipe == team]["Absence 3"].tolist()[0].upper().split("/")
        key4 = params[params.Equipe == team]["Absence 4"].tolist()[0].upper().split("/")

        abs1 = "O"
        abs2 = "O"
        abs3 = "O"
        abs4 = "O"

        for elt in key1:
            regex = r"\D*\t*" + elt + r"\t*\D*"
            for player in listeA:
                search = re.findall(regex, player)
                if len(search) > 0:
                    abs1 = None
                    break

        for elt in key2:
            regex = r"\D*\t*" + elt + r"\t*\D*"
            for player in listeA:
                search = re.findall(regex, player)
                if len(search) > 0:
                    abs2 = None
                    break

        for elt in key3:
            regex = r"\D*\t*" + elt + r"\t*\D*"
            for player in listeA:
                search = re.findall(regex, player)
                if len(search) > 0:
                    abs3 = None
                    break

        for elt in key4:
            regex = r"\D*\t*" + elt + r"\t*\D*"
            for player in listeA:
                search = re.findall(regex, player)
                if len(search) > 0:
                    abs4 = None
                    break

        match["Ligue"] = champ
        match["Date"] = date_game
        match["Equipe"] = team
        match["Equipe adverse"] = adv
        match["Home / Away"] = lieu
        match["XG1"] = float(xg1)
        match["XG2"] = float(xg2)
        match["G1"] = int(g1)
        match["G2"] = int(g2)
        match["Score"] = " " + str(g1) + "-" + str(g2)
        match["Resultat"] = res
        match["Fait marquant"] = red_card
        match["Absence 1"] = abs1
        match["Absence 2"] = abs2
        match["Absence 3"] = abs3
        match["Absence 4"] = abs4
        match["XA1"] = float(xa1)
        match["XA2"] = float(xa2)
        match["Garde score"] = garde_score
        match["Revenu score"] = retour_score
        match["AMT"] = int(amt1)
        match["TCL"] = tcl1
        match["Dribbles tentés"] = int(drt1)
        match["Dribbles réussis"] = int(drr1)
        match["Prog passes"] = int(prog_pass1)
        match["Passes surface"] = int(passe_surface1)
        match["Prog drib"] = int(prog_drib1)
        match["Possession surface"] = int(poss_surface1)
        if psxg1 != "":
            match["PSXG"] = float(psxg1)
        else:
            match["PSXG"] = ""
        match["Erreurs"] = int(erreur1)
        match["Aerien win"] = float(aerien1)
        match["xg1_dead"] = xg1_dead
        match["g1_dead"] = g1_dead
        match["xg2_dead"] = xg2_dead
        match["g2_dead"] = g2_dead

        matchs.append(match)

        print("Ligue :", champ)
        print("Date :", date_game)
        print("Equipe :", team)
        print("Equipe adverse :", adv)
        print("Lieu :", lieu)
        print("G1 :", g1)
        print("G2 :", g2)
        print("XG1 :", xg1)
        print("XG2 :", xg2)
        print("Red Card :", red_card)
        print("Liste joueurs", listeA)
        print("Absence 1", abs1)
        print("Absence 2", abs2)
        print("Absence 3", abs3)
        print("Absence 4", abs4)
        print("Garde score", garde_score)
        print("Retour score", retour_score)
        print("XA1", xa1)
        print('Dribbles tentés', drt1)
        print('Dribbles réussis', drr1)
        print("Passes surface", passe_surface1)
        print("Possession surface", poss_surface1)
        print("PSXG", psxg1)
        print("Erreur", erreur1)
        print("Aerien", aerien1)
        print("Prog passes", prog_pass1)
        print("Prog drib", prog_drib1)
        print("xg1_dead", xg1_dead)
        print("g1_dead", g1_dead)
        print("xg2_dead", xg2_dead)
        print("g2_dead", g2_dead)

    df = pd.DataFrame(matchs)
    df.sort_index(axis=0, ascending=False, inplace=True)
    df.to_csv('/Users/mathieulengrand/Desktop/Modele foot/Modèles/Output/' + team + '.csv', index=False,
              encoding='utf-8')
    print(df)
