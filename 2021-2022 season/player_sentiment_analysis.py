#this script is to get actual players name every match and carry out sentiment analysis on what people have to say on them at twitter
#this script also calcualte the actual game performance for every post match


from calculate_weekly_performance import player_names
import tweepy as tw
import configparser
import os
import pandas as pd
from datetime import date
import datetime
import time
import sys

import re

from textblob import TextBlob
from nltk.corpus import stopwords
from textblob import Word
import nltk
from wordcloud import STOPWORDS
from nltk.stem import WordNetLemmatizer
from nltk.stem import LancasterStemmer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


from sqlalchemy import create_engine 
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


        #get api keys
        self.user=self.config['database']['user']
        self.password=self.config['database']['password']
        self.host=self.config['database']['host']
        self.database=self.config['database']['database']
        self.engine = create_engine("mysql+pymysql://" + self.user+ ":" + self.password + "@" + self.host + "/" + self.database)


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
        self.df=pd.DataFrame(df)
        


class Cleaning_tweet(Tweets):

    #remove any emojis in the tweet since we do not need it
    #update: vader performs well with emojis and emojis also plays an important role in the sentiment of the tweet
    def remove_emoji(self,tweet):
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                            "]+", flags=re.UNICODE)
        cleaned_tweet=emoji_pattern.sub(r'', tweet)
        tweet=cleaned_tweet

    #cleaning tweets to get 'important' text
    def clean_tweets(self):
        self.stop=stopwords.words('english')
        self.ls = LancasterStemmer()

        #stemming the tweet
        self.df['tweet']=self.df['tweet'].apply(lambda x: self.ls.stem(x))
        self.df['tweet']=self.df['tweet'].apply(lambda tweet:re.sub(r"https?:\/\/\S+","",tweet))

        
        
class Sentiment(Cleaning_tweet):

    #to categorize the tweets based on their sentiments
    def calculate_sentiment(self):
        print('-----------CLASSIFYING INTO SENTIMENTS-------')
        self.vader=SentimentIntensityAnalyzer()
        self.sentiment=pd.json_normalize(self.df['tweet'].apply(lambda tweet:self.vader.polarity_scores(str(tweet))))
        self.df=pd.concat([self.df,self.sentiment],axis=1)

        self.df['sentiment']=self.df['compound'].apply(lambda x: 'positive' if x>=0.05 else ('neutral' if -0.05<x<0.05 else 'negative'))
        print(self.df)


class Database(Sentiment):

    def update_database(self):
        try:
            self.df.to_sql('player_sentiment3',con=self.engine,if_exists='append',index=False)
            print("Done update to database")
        except:
            print("Cannot connect to database")


tweets=Database(int(input("How many tweets per player: ")),r'E:\New folder\Udemy\personal data science projects\Arsenal\2021-2022 season\arsenal_match_preds\2021-2022 season\config.ini')
tweets.get_tweets()
tweets.clean_tweets()
tweets.calculate_sentiment()
tweets.update_database()
