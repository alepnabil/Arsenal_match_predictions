from os import link, name
import pandas as pd
import requests
from bs4 import BeautifulSoup
from requests.api import request
import selenium
from selenium import webdriver
import time
import os

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium import webdriver
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class Predicted_lineups:

    def __init__(self,url) -> None:
        self.url=url
    #prompt ourselves the predicted formations since every week the formation maybe different

    def get_predicted_lineups(self):
        time.sleep(4)
        formation=input('-----------Enter formation : ')

        Predicted_lineups=[]
        request=requests.get(self.url)
        soup=BeautifulSoup(request.content,'html.parser')

        #we will probably scrape other teams that has the same formation
        predicted_lineups=soup.select('div.formation.formation-'+str(formation)+' span')


        #so we will filter and get only arsenal players
        for preds in (predicted_lineups):
            if preds.text=='':
                pass
            else:
                #print(x.text)
                Predicted_lineups.append(preds.text)

        #SPECIAL CASE FOR BEN WHITE SINCE HIS NAME IS COMMON
        for white in range(len(Predicted_lineups)):
            if Predicted_lineups[white]=='White':
                Predicted_lineups[white]='benjamin white'
                
        for gabriel in range(len(Predicted_lineups)):
            if Predicted_lineups[gabriel]=='Gabriel':
                Predicted_lineups[gabriel]='gabriel magalhaes'

        print(Predicted_lineups[:11])
        return Predicted_lineups[:11]



class Past_performance(Predicted_lineups):

    def __init__(self, url,path) -> None:
        super().__init__(url)
        self.path=path
        self.driver=webdriver.Chrome(self.path)


    def search_players_links(self):
        #get the names
        name=self.get_predicted_lineups()
        #links for previous ratings
        player_ratings_link=[]

        for nme in name:
            time.sleep(3)
            self.driver.get('https://www.whoscored.com/Search/?t='+str(nme))
            self.soup=BeautifulSoup(self.driver.page_source,'html.parser')
     
            player=self.soup.find_all('a',class_='iconize iconize-icon-left',href=True,limit=1)
            #player=self.soup.select_one('a.iconize.iconize-icon-left')['href']
            for x in player:
                print(x['href'])
                player_ratings_link.append(x['href'])

        print(player_ratings_link)


calculate_past_performance=Past_performance('https://www.fantasyfootballscout.co.uk/team-news/',ChromeDriverManager().install())
calculate_past_performance.search_players_links()