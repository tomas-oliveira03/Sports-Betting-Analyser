import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

options = webdriver.ChromeOptions()
options.set_capability(
    'goog:loggingPrefs', {
        "performance": "ALL",
        "browser": "ALL"
    }
)

service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)


goodGames=[]
gamesNotPossible=[]


# SofaScore URL
driver.get('https://www.sofascore.com')



# Deal with cookies popup
try:
    cookie_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[2]/div[1]/div[2]/div[2]/button[1]"))
    )
    cookie_button.click()
    print("Cookie popup accepted.")
except Exception as e:
    print(f"An error occurred: {e}")

    

# Get all URLs from today's games
allGames=[]
games = driver.find_element(By.XPATH, '/html/body/div[1]/main/div/div[2]/div[2]/div/div[3]')

for game in games.find_elements(By.XPATH, './div'):
    anchor_tags = game.find_elements(By.TAG_NAME, 'a')
    for anchor_tag in anchor_tags:
        
        
        href = anchor_tag.get_attribute('href')
        
        if "match" in href:
            
            # Removing live or finished games
            try:
                anchor_tag.find_element(By.XPATH, './/bdi[contains(text(), "-")]')
                allGames.append(href)
            except:
                pass


## GAME PAGE ##########################################
for game in allGames:
    print("Link: ",game)


    driver.get(game)

    Team1 = {}
    Team2 = {}
    
    try:

        # Fetch Teams Names
        Team1["name"]=driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div/div[1]/div/a/div/div/bdi").text
        Team2["name"]=driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div/div[3]/div/a/div/div/bdi").text
        ####################


        # Fetch Teams Odds
        Team1["odd"]= float(driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/a[1]/div/span").text)
        Team2["odd"]= float(driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/a[3]/div/span").text)
        ####################


        # Fetch Teams Rankings
        rankings = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div[2]/div[1]/div[2]/div[3]/div/div[2]/div/div[1]/div[3]/div')
        anchorTags = rankings.find_elements(By.TAG_NAME, 'a')

        for team in anchorTags:
            team_name_element = team.find_element(By.TAG_NAME, 'div')
            name = team_name_element.text.split('\n')[1]
            ranking = team_name_element.text.split('\n')[0]
            
            if name in Team1["name"]:
                Team1["ranking"] = int(ranking)
            elif name in Team2["name"]:
                Team2["ranking"] = int(ranking)
        ####################

        print(Team1)
        print(Team2)
        print()


        # Algorithm to determine if the odd is good or not
        if Team1["ranking"] < Team2["ranking"]:
            # Team1 is ranked higher
            if abs(Team1["ranking"]-Team2["ranking"])>5 and Team1["odd"]>1.4:
                Team1["link"]=game
                goodGames.append(Team1)
                print("Team1 is a good bet")
            else:
                pass
                print("Team1 is not a good bet")
            
        else:
            # Team2 is ranked higher
            if abs(Team1["ranking"]-Team2["ranking"])>5 and Team2["odd"]>1.4:
                Team2["link"]=game
                goodGames.append(Team2)
                print("Team2 is a good bet")
            else:
                print("Team2 is not a good bet")
    
    except:
        gamesNotPossible.append(game)
        print("Game is not possible.")
            
    print("------------------\n")
##print()
##print(Team1)
##print(Team2)
    
    
print(goodGames)
print()
print(gamesNotPossible)

# Create a file called games.txt
with open('GoodGames.txt', 'w') as file:
    # Write the link of each game in goodGames to the file
    for game in goodGames:
        file.write(game['link'] + '\n')
        
with open('NotGames.txt', 'w') as file:
    # Write the link of each game in goodGames to the file
    for game in gamesNotPossible:
        file.write(game + '\n')

    
# Close the browser
driver.quit()

