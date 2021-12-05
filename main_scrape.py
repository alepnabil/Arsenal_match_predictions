import pandas as pd
import requests
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
import time

from selenium.webdriver.chrome.webdriver import WebDriver



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
        return individual_links


    def go_to_each_match_report(self):
        links=self.match_report_links()
        #print(links)
        return links


#inherit each match link from main webpage
# will go to each link and scrape the gk,def,mid,attack rating
class Individual_links(Scrape):

    def __init__(self, path):
        super().__init__(path)
        self.driver=webdriver.Chrome(self.path)
    
    #get each match link
    #then navigate to each match link
    #get the data we want
    def navigate_to_each_link(self):
        match_link=self.match_report_links()
        #the first LINK for testing
        match_link=match_link[0]
        first_indv_link='https://www.whoscored.com' + match_link[0:21]+ 'Statistics'+ match_link[21:]
        #print(first_indv_link)

        #DRIVER TO GO TO EACH INDIVIDUAL LINKS
        self.driver2=webdriver.Chrome(self.path)
        time.sleep(3)
        self.driver2.get(first_indv_link)

        #LOOKS LIKE WE HAVE TO KEEP CHANGING FROM HTML.PARSER TO LXML EVERYTIME WE RUN THE SCRIPT?????
        self.soup2=BeautifulSoup(self.driver2.page_source,'lxml')
        time.sleep(3)

    def player_ratings(self):

        Players_list=[]
        Player_rating=[]
        #get player name
        print('getting player name and ratings')
        try:
            #NEED TO KEEP CHANGING FROM HTML.PARSER TO LXML EVERYTIME RUN THE SCRAPE
            time.sleep(3)
            player_name=self.soup2.select('a.player-link span.iconize.iconize-icon-left')
            #print('------------getting player name and ratings-----------')
            for x in player_name:
                print(x.text)
                Players_list.append(x.text)

        except:
            print('NO ELEMENT')

        print(Players_list)

        #Player={
               # 'name':player_name,
               # 'rating':player_rating
                #}
        
        #print(Player)


class Gk():
    pass

class Def():
    pass

class Mid():
    pass

class Attack():
    pass


#scrape=Scrape('C:\\Program Files (x86)\\chromedriver.exe')
indv_link=Individual_links('C:\\Program Files (x86)\\chromedriver.exe')
indv_link.request_page()
indv_link.navigate_to_each_link()
indv_link.player_ratings()