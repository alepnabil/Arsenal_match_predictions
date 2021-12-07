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


Stats_table=[]
Ratings=[]
driver=webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://www.whoscored.com/Matches/1549539/LiveStatistics/England-Premier-League-2021-2022-Brentford-Arsenal')
soup=BeautifulSoup(driver.page_source,'html.parser')

#player_name=soup.find_all('a')
driver.implicitly_wait(3)
#player_name=soup.select('span iconize.iconize-icon-left')
#player_name=soup.find_all('a',class_='player-link',href=True)

#this gets all the names but cant get the players name text
#player_name=soup.select('a span.iconize.iconize-icon-left')

#stats_table = soup.find_all("div", {"id": "live-player-away-stats"})
#tats_table = soup.find_all("tbody", {"id": "player-table-statistics-body"})
#stats_table = soup.find_all("td", {"class": "rating"})


driver.implicitly_wait(5)
#doesnt get the second table data
#stats_table = soup.find_all("table", {"id": "top-player-stats-summary-grid"})

#doesnt get the second table as well
#stats_table = soup.find("tbody", {"id": "player-table-statistics-body"})

#doesnt get anything
#stats_table=soup.select('tbody#player-table-statistics-body')

#gets everything like ours
#stats_table=soup.select('td.rating')
#print(stats_table)
#doesnt get all the names at all
#names=soup.select('td.col12-lg-2.col12-m-3.col12-s-4.col12-xs-5.grid-abs.overflow-text')

names=soup.find_all("span", {"class": "iconize iconize-icon-left"})



divs = soup.select('div#statistics-table-away-summary a span.iconize.iconize-icon-left')
for div in divs:
    player = div.text
    Stats_table.append(player)
    #print(player)

rs = soup.select('div#statistics-table-away-summary td.rating')
for r in rs:
    rating = r.text
    #print(rating)
    Ratings.append(rating)


#.find("tbody", {"id": "player-table-statistics-body"})
#print('scraping player name')
#for x in names:
    #data=x.find("td", {"class": "rating"}).text
    #nama=x.find('span')
 #   Stats_table.append(x.string)


    #driver.implicitly_wait(5)
    #name=x.find('span')
    #print(x.string)
    #print(x.text)
    #print('---------')
    #driver.implicitly_wait(3)

    #print(x.string)

print(Stats_table)
print(Ratings)