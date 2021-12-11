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
            url='https://www.whoscored.com/'+player_link

            self.driver.get(url)
            time.sleep(3)
            self.soup2=BeautifulSoup(self.driver.page_source,'html.parser')

            check_epl=self.soup2.find_all('div',class_='table-body')

            #go to the table
            for y in check_epl:
                #select all rows
                get_only_epl=y.find_all('a',class_='iconize iconize-icon-left tournament-link',href=True)
                #check if it's the epl or not
                for tag in get_only_epl:
                    print(tag)
                    #get only the epl's ratings by checking it's link
                    if 'Premier-League' in tag['href']:
                        ratings=tag.find('div',class_='col12-lg-1 col12-m-1 col12-s-1 col12-xs-1 divtable-data col-data-rating')
                        print(ratings)
                    else:
                        pass
            

            #THE PROBLEM HERE IS THAT IT GETS ALL THE RATINGS WHICH IS MIXED WITH INTERNATIONAL MATCHES
            ratings=self.soup2.select('div.col12-lg-1.col12-m-1.col12-s-1.col12-xs-1.divtable-data.col-data-rating')

            #for rat in ratings[-6:]:
            #    print(rat.text)
            #    temp_ratings.append(float(rat.text))

            #avg_past_performance=sum(temp_ratings)/len(temp_ratings)
            #print(f'THE PAST AVERAGE PERFORMANCE FOR PLAYER {link} IS {avg_past_performance}')


calculate_past_performance=Past_performance('https://www.fantasyfootballscout.co.uk/team-news/',ChromeDriverManager().install())
#calculate_past_performance.search_players_links()
calculate_past_performance.calculate_player_ratings()