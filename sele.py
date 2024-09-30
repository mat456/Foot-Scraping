from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import re
from setup import recup_dead_stats

def recup_onglets(lien):
    driver = webdriver.Safari()
    driver.get(lien)
    driver.maximize_window()

    time.sleep(3)



    #banniere = driver.find_element(By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[3]')
   # driver.execute_script("arguments[0].click();", banniere)



    passes = driver.find_elements(By.XPATH,"//*[contains(text(), 'Passes')]")

    driver.execute_script("arguments[0].scrollIntoView();", passes[0])
    driver.execute_script("arguments[0].click();", passes[0])
    driver.execute_script("arguments[0].scrollIntoView();", passes[3])
    driver.execute_script("arguments[0].click();", passes[3])

    soup = BeautifulSoup(driver.page_source, "html.parser")

    exp = soup.body.findAll('table')
    id_name = re.findall(r"stats_\S*_passing", str(exp))

    passes_surface = soup.find_all('table', attrs={"id": id_name[0]})[0].find_all("tr")
    passes_surface1 = passes_surface[len(passes_surface) - 1].find_all('td', attrs={"class": "right"})[21].get_text()
    xag1 = passes_surface[len(passes_surface) - 1].find_all('td', attrs={"class": "right"})[17].get_text()
    xa1 = passes_surface[len(passes_surface) - 1].find_all('td', attrs={"class": "right"})[18].get_text()
    xa1 = round(float(xag1) + float(xa1), 1)

    passes_surface = soup.find_all('table', attrs={"id": id_name[2]})[0].find_all("tr")
    passes_surface2 = passes_surface[len(passes_surface) - 1].find_all('td', attrs={"class": "right"})[21].get_text()
    xag2 = passes_surface[len(passes_surface) - 1].find_all('td', attrs={"class": "right"})[17].get_text()
    xa2 = passes_surface[len(passes_surface) - 1].find_all('td', attrs={"class": "right"})[18].get_text()
    xa2 = round(float(xag2) + float(xa2), 1)



    possession = driver.find_elements(By.XPATH, "//*[contains(text(), 'Possession')]")

    driver.execute_script("arguments[0].scrollIntoView();", possession[2])
    driver.execute_script("arguments[0].click();", possession[2])
    driver.execute_script("arguments[0].scrollIntoView();", possession[1])
    driver.execute_script("arguments[0].click();", possession[1])

    soup = BeautifulSoup(driver.page_source, "html.parser")

    exp = soup.body.findAll('table')
    id_name = re.findall(r"stats_\S*_possession", str(exp))

    poss_surface = soup.find_all('table', attrs={"id": id_name[0]})[0].find_all("tr")
    poss_surface1 = poss_surface[len(poss_surface) - 1].find_all('td', attrs={"class": "right"})[19].get_text()
    poss_surface = soup.find_all('table', attrs={"id": id_name[1]})[0].find_all("tr")
    poss_surface2 = poss_surface[len(poss_surface) - 1].find_all('td', attrs={"class": "right"})[19].get_text()

    defense = driver.find_elements(By.XPATH, "//*[contains(text(), 'Actions défensives')]")

    driver.execute_script("arguments[0].scrollIntoView();", defense[0])
    driver.execute_script("arguments[0].click();", defense[0])
    driver.execute_script("arguments[0].scrollIntoView();", defense[1])
    driver.execute_script("arguments[0].click();", defense[1])

    soup = BeautifulSoup(driver.page_source, "html.parser")

    exp = soup.body.findAll('table')
    id_name = re.findall(r"stats_\S*_defense", str(exp))

    erreur = soup.find_all('table', attrs={"id": id_name[0]})[0].find_all("tr")
    erreur1 = erreur[len(erreur) - 1].find_all('td', attrs={"class": "right"})[17].get_text()
    erreur = soup.find_all('table', attrs={"id": id_name[1]})[0].find_all("tr")
    erreur2 = erreur[len(erreur) - 1].find_all('td', attrs={"class": "right"})[17].get_text()

    aerien = driver.find_elements(By.XPATH, "//*[contains(text(), 'Statistiques diverses')]")

    driver.execute_script("arguments[0].scrollIntoView();", defense[0])
    driver.execute_script("arguments[0].click();", defense[0])
    driver.execute_script("arguments[0].scrollIntoView();", defense[1])
    driver.execute_script("arguments[0].click();", defense[1])

    soup = BeautifulSoup(driver.page_source, "html.parser")

    exp = soup.body.findAll('table')
    id_name = re.findall(r"stats_\S*_misc", str(exp))

    aerien = soup.find_all('table', attrs={"id": id_name[0]})[0].find_all("tr")
    aerien1 = aerien[len(aerien) - 1].find_all('td', attrs={"class": "right"})[17].get_text()
    aerien = soup.find_all('table', attrs={"id": id_name[1]})[0].find_all("tr")
    aerien2 = aerien[len(aerien) - 1].find_all('td', attrs={"class": "right"})[17].get_text()

    xg1_dead, g1_dead = recup_dead_stats(driver, 1)
    xg2_dead, g2_dead = recup_dead_stats(driver, 2)





    driver.close()

    return passes_surface1, passes_surface2, poss_surface1, poss_surface2, xa1, xa2, erreur1, erreur2, aerien1, aerien2, xg1_dead, g1_dead, xg2_dead, g2_dead


