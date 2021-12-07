from os import link, name
import pandas as pd
import requests
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
import time
import os
from requests_html import HTMLSession

from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager



driver=webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://www.whoscored.com/Matches/1549539/LiveStatistics/England-Premier-League-2021-2022-Brentford-Arsenal')
soup=BeautifulSoup(driver.page_source,'html.parser')

#player_name=soup.find_all('a')
driver.implicitly_wait(3)
#player_name=soup.select('span iconize.iconize-icon-left')
player_name=soup.find_all('a',class_='player-link',href=True)
print('scraping player name')
#print(player_name)
for x in player_name:
    driver.implicitly_wait(5)
    name=x.find('span')
    print(name.text)
    #print(x.text)
    #print('---------')
    driver.implicitly_wait(3)

    #print(x.string)
