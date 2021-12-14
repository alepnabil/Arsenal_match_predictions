#this script scrapes the predicted line up for upcoming matches and calculate their past performance for 6 games


from os import link, name
import pandas as pd
import requests
from bs4 import BeautifulSoup
from requests.api import request
import selenium
from selenium import webdriver
import time
import os
import numpy as np

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium import webdriver
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class Predicted_lineups:

    def __init__(self,url):
        self.url=url
    #prompt ourselves the predicted formations since every week the formation maybe different

    #scrape predicted lineups and returns the names
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

    #get the predicted lineups names
    #pass the links to the calculate function
    def search_players_links(self):
        #get the names
        name=self.get_predicted_lineups()
        #links for previous ratings
        player_ratings_link=[]

        for nme in name:
            time.sleep(3)
            #go to the search page
            self.driver.get('https://www.whoscored.com/Search/?t='+str(nme))
            self.soup=BeautifulSoup(self.driver.page_source,'html.parser')
            
            #get the first link of the players(arsenal players supposedly is the first one)
            player=self.soup.find_all('a',class_='iconize iconize-icon-left',href=True,limit=1)
            #get only the links
            for x in player:
                print(x['href'])
                player_ratings_link.append(x['href'])

        #print(player_ratings_link)
        #self.calculate_player_ratings(player_ratings_link,name)
        return player_ratings_link,name

    #go to each link and calculate past 6 games performances
    def calculate_player_ratings(self):

        links,names=self.search_players_links()
        player_ratings=[]
        #nagivate to each link and scrape past ratings and put inside a csv

        for link in range(0,len(links)):
            temp_ratings=[]
            print(f'------GOING TO PLAYER {link} PAGE----')
            player_link=links[link]
            Player_link=player_link.replace('Show','MatchStatistics')
            url='https://www.whoscored.com/'+Player_link

            self.driver.get(url)
            time.sleep(3)
            premier_league=self.driver.find_element_by_xpath('//*[@id="tournamentOptions"]/dd[1]/a')
            premier_league.click()
            time.sleep(2)
            self.soup2=BeautifulSoup(self.driver.page_source,'html.parser')

            rating=self.soup2.find_all('td',class_='rating')

            for rat in rating[:6]:
                print(rat.text)
                temp_ratings.append(float(rat.text))
      

            avg_past_performance=sum(temp_ratings)/len(temp_ratings)
            player_ratings.append(avg_past_performance)
            print(f'THE PAST AVERAGE PERFORMANCE FOR PLAYER {link} IS {avg_past_performance}')


        return player_ratings,names

    #function to update to a csv
    def update_to_excel(self):
        player_ratings,names=self.calculate_player_ratings()

        Player_ratings=pd.DataFrame(player_ratings)
        Player_names=pd.DataFrame(names)

        df=pd.concat([Player_ratings,Player_names],axis=1)
        print(df)

        df.to_csv(r'E:\New folder\Udemy\personal data science projects\Arsenal\2021-2022 season\arsenal_match_preds\2021-2022 season\predicted_lineups_past_performance.csv')


calculate_past_performance=Past_performance('https://www.fantasyfootballscout.co.uk/team-news/',ChromeDriverManager().install())
#calculate_past_performance.search_players_links()
calculate_past_performance.update_to_excel()