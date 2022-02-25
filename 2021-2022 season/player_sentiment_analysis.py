#this script is to get actual players name every match and carry out sentiment analysis on what people have to say on them at twitter

from calculate_weekly_performance import player_names
import tweepy as tw
import configparser
import os
import pandas as pd
from datetime import date
import datetime
import time
import sys


class Tweets():

    def __init__(self,count,file_path):
        #read from api keys file
        self.config=configparser.ConfigParser()
        self.config_file_path=file_path
        self.config.read(self.config_file_path)

        #get api keys
        self.api_key=self.config['twitter']['api_key']
        self.api_key_secret=self.config['twitter']['api_key_secret']
        self.access_token_project=self.config['twitter']['access_token_project']
        self.access_token_secret=self.config['twitter']['access_token_secret']

        #set the settings for which tweet to get
        self.today = date.today()
        self.date_until = str(self.today.strftime("%Y-%m-%d"))
        self.language='en'
        self.count=count

    def authorize_api(self):
        try:
            #authorization for tweepy with api tokens
            self.auth = tw.OAuthHandler(self.api_key, self.api_key_secret)
            self.auth.set_access_token(self.access_token_project, self.access_token_secret)
            self.api=tw.API(self.auth, wait_on_rate_limit=True)
        except e:
            print("Problem using twitter APIs")
    


    def get_tweets(self):
        #call authorize function
        self.authorize_api()
        #empty list for our dateframe
        df=[]

        #loop through the players that play the match
        for player in player_names:
            search_words=player
            try:
                #search for tweets mentioning the player
                tweets = self.api.search_tweets(q=search_words+'-filter:retweets',
                                    until=self.date_until,
                                    result_type='recent',
                                    lang=self.language,
                                    count=self.count
                                    )
                print('\n')
                print(f'______________________getting tweets about {player}________________________')
                for tweet in tweets:
                    #should get tweet which contain long text so that it is more meaningful
                    if len(tweet.text)>10:
                            tweet_text=tweet.text
                            tweet_date=tweet.created_at
                            #append each tweet to every row
                            row={'date':tweet_date,'player':player,'tweet':tweet_text}
                            df.append(row)
                time.sleep(2)
            except :
                sys.exit("Problem using twitter APIs")
        df=pd.DataFrame(df)
        print(df)


tweets=Tweets(int(input("How many tweets per player: ")),r'E:\New folder\Udemy\personal data science projects\Arsenal\2021-2022 season\arsenal_match_preds\2021-2022 season\config.ini')
tweets.get_tweets()