import pandas as pd
import requests
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
import time



class Scrape():

    def __init__(self,path):
        self.path=path
        self.driver=webdriver.Chrome(self.path)
    
    def request_page(self):
        self.driver.get('https://www.whoscored.com/Teams/13/Fixtures/England-Arsenal')
        self.soup=BeautifulSoup(self.driver.page_source,'html.parser')
        time.sleep(3)
    
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
        print(links)
        

class Gk():
    pass

class Def():
    pass

class Mid():
    pass

class Attack():
    pass


scrape=Scrape('C:\\Program Files (x86)\\chromedriver.exe')
scrape.request_page()
scrape.go_to_each_match_report()
