from os import link, name
import pandas as pd
import requests
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
import time
import os

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium import webdriver
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


formation=input('Enter formation : ')
url='https://www.fantasyfootballscout.co.uk/team-news/'

request=requests.get(url)

soup=BeautifulSoup(request.content,'html.parser')

#we will probably scrape other teams that has the same formation
predicted_lineups=soup.select('div.formation.formation-'+str(formation)+' span')
print('div.formation.formation-'+str(formation)+' span')
Predicted_lineups=[]


#so we will filter and get only arsenal players
for x in (predicted_lineups):
    if x.text=='':
        pass
    else:
        #print(x.text)
        Predicted_lineups.append(x.text)

print(Predicted_lineups[:11])
