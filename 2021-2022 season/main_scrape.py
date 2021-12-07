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



#inherit each match link from main webpage
# will go to each link and scrape the gk,def,mid,attack rating
class Individual_links(Scrape):

    def __init__(self, path):
        super().__init__(path)
        #self.driver=webdriver.Chrome(self.s)
        
    #get each match link
    #then navigate to each match link
    #get the data we want
    def navigate_to_each_link(self):
        match_links=self.match_report_links()
        for link in range (0,len(match_links)):
            #match_link=self.match_report_links()
            #the first LINK for testing
            match_link=match_links[link]
            first_indv_link='https://www.whoscored.com' + match_link[0:21]+ 'Statistics'+ match_link[21:]
            print(first_indv_link)
            #print(first_indv_link)

            #DRIVER TO GO TO EACH INDIVIDUAL LINKS
            self.driver2=webdriver.Chrome(self.path)
            self.driver2.implicitly_wait(25)
            self.driver2.get(first_indv_link)
            self.driver2.implicitly_wait(25)
            time.sleep(10)
            #LOOKS LIKE WE HAVE TO KEEP CHANGING FROM HTML.PARSER TO LXML EVERYTIME WE RUN THE SCRIPT?????
            #self.soup2=BeautifulSoup(self.driver2.page_source,'lxml')
            #self.soup2=BeautifulSoup(self.driver2.page_source,'xml')
            self.soup2=BeautifulSoup(self.driver2.page_source,'html.parser')
            #self.soup2=BeautifulSoup(self.driver2.page_source,'html5lib')
            self.driver2.implicitly_wait(25)
            self.player_ratings(link)

    def player_ratings(self,link):
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
   
        df.to_csv('D:\\Udemy\\personal data science projects\\Arsenal\\2021-2022 season\\arsenal_match_preds\\2021-2022 season\\'+str(link+1)+'_match.csv')
        


#SCRAPE EACH POSITIONS RATINGS
class Gk():

    def __init__(self,page):
        self.page=page
        
    
    #read that csv
    #calculate their ratings
    def calculate_ratings(self):
        print('-----CALCULATING GOALKEEPER AVERAGE RATINGS FOR ', str(self.page +1 ), 'MATCH------')
        time.sleep(2)
        df=pd.read_csv('D:\\Udemy\\personal data science projects\\Arsenal\\2021-2022 season\\arsenal_match_preds\\2021-2022 season\\'+str(self.page+1)+'_match.csv')
        df=df.drop(df.columns[[0]], axis=1)
        df.columns=['players','ratings']

        #cleaning through our data
        df['ratings']=df['ratings'].replace('-',0)
        df['ratings']=df['ratings'].apply(lambda x:(float(x)))

        #take only goalkeepers which play(ratings>0)
        goalkeeper=df[(df['players'].str.lower().str.contains('leno')&df['ratings']>0)|
        (df['players'].str.lower().str.contains('ramsdale')&df['ratings']>0)]
    
        print(goalkeeper)
        #for example both leno and ramsdale play that match, then we just find the average rating for the goalkeeper position
        count=len(goalkeeper)
        avg_gk_ratings=sum(goalkeeper['ratings'])/count
        print("AVERAGE GK RATINGS:",avg_gk_ratings)

   
class Def(Gk):


    def calculate_ratings(self):
        print('-----CALCULATING DEFENDER AVERAGE RATINGS FOR ', str(self.page +1 ), 'MATCH------')
        time.sleep(2)
        df=pd.read_csv('D:\\Udemy\\personal data science projects\\Arsenal\\2021-2022 season\\arsenal_match_preds\\2021-2022 season\\'+str(self.page+1)+'_match.csv')
        df=df.drop(df.columns[[0]], axis=1)
        df.columns=['players','ratings']

        #cleaning through our data
        df['ratings']=df['ratings'].replace('-',0)
        df['ratings']=df['ratings'].apply(lambda x:(float(x)))

    


        #take only defenders which play(ratings>0)
        defends=df[(df['players'].str.lower().str.contains('tierney')& df['ratings']>0)|
        (df['players'].str.lower().str.contains('white')& df['ratings']>0)|
        (df['players'].str.lower().str.contains('gabriel')& df['ratings']>0)|
        (df['players'].str.lower().str.contains('holding')& df['ratings']>0)|
        (df['players'].str.lower().str.contains('cedric')& df['ratings']>0)|
        (df['players'].str.lower().str.contains('tomiyasu')& df['ratings']>0)|
        (df['players'].str.lower().str.contains('tavares')& df['ratings']>0)|
        (df['players'].str.lower().str.contains('chambers')& df['ratings']>0)|
        (df['players'].str.lower().str.contains('mari')& df['ratings']>0)|
        (df['players'].str.lower().str.contains('kolasinac')& df['ratings']>0)]
        print(defends)
        #for example both leno and ramsdale play that match, then we just find the average rating for the goalkeeper position
        count=len(defends)
        avg_def_ratings=sum(defends['ratings'])/count
        print("AVERAGE DEFENDER RATINGS : " , avg_def_ratings)

class Mid(Gk):


     def calculate_ratings(self):
        print('-----CALCULATING MIDFIELDERS AVERAGE RATINGS FOR ', str(self.page +1 ), 'MATCH------')
        time.sleep(2)
        df=pd.read_csv('D:\\Udemy\\personal data science projects\\Arsenal\\2021-2022 season\\arsenal_match_preds\\2021-2022 season\\'+str(self.page+1)+'_match.csv')
        df=df.drop(df.columns[[0]], axis=1)
        df.columns=['players','ratings']
        
        #cleaning through our data
        df['ratings']=df['ratings'].replace('-',0)
        df['ratings']=df['ratings'].apply(lambda x:(float(x)))

        #take only midfielders which play(ratings>0)
        midfields=df[(df['players'].str.lower().str.contains('partey')& df['ratings']>0)|
        (df['players'].str.lower().str.contains('smith')& df['ratings']>0)|
        (df['players'].str.lower().str.contains('saka')& df['ratings']>0)|
        (df['players'].str.lower().str.contains('odegaard')& df['ratings']>0)|
        (df['players'].str.lower().str.contains('maitland')& df['ratings']>0)|
        (df['players'].str.lower().str.contains('lokonga')& df['ratings']>0)|
        (df['players'].str.lower().str.contains('elneny')& df['ratings']>0)|
        (df['players'].str.lower().str.contains('xhaka')& df['ratings']>0)]
        print(midfields)

        count=len(midfields)
        avg_mid_ratings=sum(midfields['ratings'])/count
        print('AVERAGE MIDFIELD RATINGS : ', avg_mid_ratings)

class Attack(Gk):

    def calculate_ratings(self):
        print('-----CALCULATING FORWARDS AVERAGE RATINGS FOR ', str(self.page +1 ), 'MATCH------')
        time.sleep(2)
        df=pd.read_csv('D:\\Udemy\\personal data science projects\\Arsenal\\2021-2022 season\\arsenal_match_preds\\2021-2022 season\\'+str(self.page+1)+'_match.csv')
        df=df.drop(df.columns[[0]], axis=1)
        df.columns=['players','ratings']

        #cleaning through our data
        df['ratings']=df['ratings'].replace('-',0)
        df['ratings']=df['ratings'].apply(lambda x:(float(x)))

        #take only forwards which play(ratings>0)
        forwards=df[(df['players'].str.lower().str.contains('lacazette')& df['ratings']>0)|
        (df['players'].str.lower().str.contains('aubameyang')& df['ratings']>0)|
        (df['players'].str.lower().str.contains('Pépé')& df['ratings']>0)|
        (df['players'].str.lower().str.contains('balogun')& df['ratings']>0)|
        (df['players'].str.lower().str.contains('nketiah')& df['ratings']>0)|
        (df['players'].str.lower().str.contains('martinelli')& df['ratings']>0)|
        (df['players'].str.lower().str.contains('nelson')& df['ratings']>0)]
        print(forwards)


        count=len(forwards)
        avg_frwd_ratings=sum(forwards['ratings'])/count
        print('AVERAGE FORWARDS RATING : ', avg_frwd_ratings)



#scrape=Scrape('C:\\Program Files (x86)\\chromedriver.exe')
#indv_link=Individual_links('C:\\Program Files (x86)\\chromedriver.exe')
#indv_link.request_page()
#indv_link.navigate_to_each_link()
#indv_link.player_ratings()

indv_link=Individual_links(ChromeDriverManager().install())
indv_link.request_page()
indv_link.navigate_to_each_link()
#indv_link.player_ratings()

for i in range(0,5):
  
    goalkeeper=Gk(i)
    goalkeeper.calculate_ratings()

    defender=Def(i)
    defender.calculate_ratings()

    midfield=Mid(i)
    midfield.calculate_ratings()

    forwards=Attack(i)
    forwards.calculate_ratings()


