#this script gets each week's game actual performance

from webdriver_manager.chrome import ChromeDriverManager
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



class Scrape():

    def __init__(self,path):
        self.path=path
        self.driver=webdriver.Chrome(self.path)
    
    def request_page(self):
        self.driver.get('https://www.whoscored.com/Teams/13/Fixtures/England-Arsenal')
        self.soup=BeautifulSoup(self.driver.page_source,'html.parser')
        time.sleep(3)

    #FIND ALL THE MATCH LINKS IN THE MAIN WEBPAGE
    def match_report_links(self):
        individual_links=[]
        print('-----GETTING ALL MATCH LINKS--------')
        time.sleep(3)
        try:
            #this will get all the mathes link. we only want the premier leagues
            match_links=self.soup.find_all('a',{"class": "horiz-match-link result-1"},href=True)
            for x in match_links:
                #will get only the premier league links
                if 'Premier-League' in x['href']:
                    #print(x['href'])
                    #print('---------')
                    individual_links.append(x['href'])
                else:
                    pass
        except:
            print('CANNOT GET ALL MATCH LINKS')
        print('-------MATCH FOUND:', len(individual_links),'-----------')
        print(individual_links)
        return individual_links

class Weekly_rating(Scrape):

    
    def __init__(self, path):
        super().__init__(path)

    #get each match link
    #then navigate to each match link
    #get the data we want
    def navigate_to_weekly_link(self):
        match_links=self.match_report_links()
        match_link=match_links[-1]
        first_indv_link='https://www.whoscored.com' + match_link[0:21]+ 'Statistics'+ match_link[21:]
        print('-----THIS WEEK MATCH : ', first_indv_link,'-----------------')
            #print(first_indv_link)

            #DRIVER TO GO TO EACH INDIVIDUAL LINKS
        self.driver2=webdriver.Chrome(self.path)
        self.driver2.implicitly_wait(25)
        self.driver2.get(first_indv_link)
        self.driver2.implicitly_wait(25)
        time.sleep(10)
 
        self.soup2=BeautifulSoup(self.driver2.page_source,'html.parser')
            #self.soup2=BeautifulSoup(self.driver2.page_source,'html5lib')
        self.driver2.implicitly_wait(25)
        self.player_ratings()

    def player_ratings(self):
        time.sleep(25)
        Players_list=[]
        Player_rating=[]

      
        #get player name
        print('getting player name and ratings')
        try:
            #NEED TO KEEP CHANGING FROM HTML.PARSER TO LXML EVERYTIME RUN THE SCRAPE
            

            print('------------getting player name-----------')
            self.driver2.implicitly_wait(25)
        
            player_name=self.soup2.select('a.player-link span.iconize.iconize-icon-left')
            for nme in player_name:
                self.driver2.implicitly_wait(25)
                #print(nme.text)
                Players_list.append(nme.text)

            player_rating=self.soup2.select('td.rating')

            print('------------getting player ratings-----------')
            self.driver2.implicitly_wait(25)
      
            for rat in player_rating:
                #print(rat.text)
                self.driver2.implicitly_wait(25)
                Player_rating.append(rat.text)
        except:
            print('NO ELEMENT')

        #Players_list_=pd.Series(Players_list)
        #Player_rating=pd.Series(Player_rating)

        Players_list=pd.DataFrame(Players_list)
        Player_rating=pd.DataFrame(Player_rating)

        
        df=pd.concat([Players_list,Player_rating],axis=1)
        #print(df)
        print(df)
   
        df.to_csv('D:\\personal project\\arsenal\\Arsenal_match_predictions\\2021-2022 season\\weekly_performance.csv')
        
weekly_link=Weekly_rating(ChromeDriverManager().install())
weekly_link.request_page()
#weekly_link.match_report_links()
weekly_link.navigate_to_weekly_link()