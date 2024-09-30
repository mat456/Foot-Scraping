import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# driver.execute_script("arguments[0].scrollIntoView(true);", team_shots_all[2])
# time.sleep(1)
# driver.execute_script("arguments[0].click();", team_shots_all[2])


def recup_dead_stats(driver, tab):
    shots = driver.find_element(By.XPATH, '//div[@id="switcher_shots"]')
    team_shots = shots.find_elements(By.XPATH, './/table[contains(@class,"stats_table")]')

    if len(team_shots) > 2:
        rows = team_shots[tab].find_elements(By.XPATH, './/tr')
        g_dead = 0
        xg_dead = 0

        for row in rows[2:]:
            try:
                type = row.find_element(By.XPATH, './/td[@data-stat="sca_1_type"]')
                outcome = row.find_element(By.XPATH, './/td[@data-stat="outcome"]')
                if "ballon arrêté" in type.text:
                    xg = row.find_element(By.XPATH, './/td[@data-stat="xg_shot"]')
                    xg_dead += float(xg.text)
                    if outcome.text == "But":
                        g_dead += 1
            except:
                pass

        xg_dead = round(xg_dead, 3)

    else:
        xg_dead = np.NaN
        g_dead = np.NaN

    return xg_dead, g_dead

# lien = "https://fbref.com/fr/matchs/2ba17e6d/Tottenham-Hotspur-Manchester-City-14-Mai-2024-Premier-League"

# driver = webdriver.Safari()
# driver.get(lien)
# driver.maximize_window()

# x, y = recup_dead_stats(driver, 1)

# print(x, y)

# driver.quit()
