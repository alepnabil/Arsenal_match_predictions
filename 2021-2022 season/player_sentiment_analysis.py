#this script is to get actual players name every match and carry out sentiment analysis on what people have to say on them at twitter



#import the name of the players that actaully played in specific match
from calculate_weekly_performance import player_names
import tweepy as tw
import configparser

#make config object to read api token from file
config=configparser.ConfigParser()
config_file_path=r'E:\New folder\Udemy\personal data science projects\Arsenal\2021-2022 season\arsenal_match_preds\2021-2022 season\config.ini'
config.read(config_file_path)

#get api tokens
api_key=config['twitter']['api_key']
api_key_secret=config['twitter']['api_key_secret']
access_token_project=config['twitter']['access_token_project']
access_token_secret=config['twitter']['access_token_secret']



try:
    #authorization for tweepy with api tokens
    auth = tw.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(access_token_project, access_token_secret)
    api=tw.API(auth, wait_on_rate_limit=True)
except Exception() as e:
    print("Problem using twitter APIs")




for x in player_names:
    print(x)

