#this script calculates the predicted lineups past performances for the last 6 games


import pandas as pd
import time


#SCRAPE EACH POSITIONS RATINGS
class Gk():

    
    #read that csv
    #calculate their ratings
    def calculate_ratings(self):
        print('-----CALCULATING GOALKEEPER AVERAGE RATINGS FOR-------')
        time.sleep(5)
        df=pd.read_csv(r'E:\New folder\Udemy\personal data science projects\Arsenal\2021-2022 season\arsenal_match_preds\2021-2022 season\predicted_lineups_past_performance.csv')
        df=df.drop(df.columns[[0]], axis=1)
        df.columns=['ratings','players']

        #cleaning through our data
        df['ratings']=df['ratings'].apply(lambda x:(float(x)))

        #take only goalkeepers which play(ratings>0)
        goalkeeper=df[(df['players'].str.lower().str.contains('leno')&df['ratings']>0)|
        (df['players'].str.lower().str.contains('ramsdale')&df['ratings']>0)]
    
        print(goalkeeper)
        #for example both leno and ramsdale play that match, then we just find the average rating for the goalkeeper position
        count=len(goalkeeper)
        avg_gk_ratings=sum(goalkeeper['ratings'])/count
        print("AVERAGE GK RATINGS:",avg_gk_ratings)
        time.sleep(5)
    

class Def(Gk):


    def calculate_ratings(self):
        print('-----CALCULATING DEFENDER AVERAGE RATINGS FOR------')
        df=pd.read_csv(r'E:\New folder\Udemy\personal data science projects\Arsenal\2021-2022 season\arsenal_match_preds\2021-2022 season\predicted_lineups_past_performance.csv')
        df=df.drop(df.columns[[0]], axis=1)
        df.columns=['ratings','players']

        #cleaning through our data
        df['ratings']=df['ratings'].apply(lambda x:(float(x)))

    


        #take only defenders which play(ratings>0)
        defends=df[(df['players'].str.lower().str.contains('tierney')& df['ratings']>0)|
        (df['players'].str.lower().str.contains('white')& df['ratings']>0)|
        (df['players'].str.lower().str.contains('magal')& df['ratings']>0)|
        (df['players'].str.lower().str.contains('holding')& df['ratings']>0)|
        (df['players'].str.lower().str.contains('soares')& df['ratings']>0)|
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
        print('-----CALCULATING MIDFIELDERS AVERAGE RATINGS FOR MATCH------')
        df=pd.read_csv(r'E:\New folder\Udemy\personal data science projects\Arsenal\2021-2022 season\arsenal_match_preds\2021-2022 season\predicted_lineups_past_performance.csv')
        df=df.drop(df.columns[[0]], axis=1)
        df.columns=['ratings','players']
        
        #cleaning through our data
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
        print('-----CALCULATING FORWARDS AVERAGE RATINGS FOR MATCH------')
        df=pd.read_csv(r'E:\New folder\Udemy\personal data science projects\Arsenal\2021-2022 season\arsenal_match_preds\2021-2022 season\predicted_lineups_past_performance.csv')
        df=df.drop(df.columns[[0]], axis=1)
        df.columns=['ratings','players']

        #cleaning through our data
        df['ratings']=df['ratings'].apply(lambda x:(float(x)))

        #take only forwards which play(ratings>0)
        forwards=df[(df['players'].str.lower().str.contains('lacazette')& df['ratings']>0)|
        (df['players'].str.lower().str.contains('aubameyang')& df['ratings']>0)|
        (df['players'].str.lower().str.contains('P??p??')& df['ratings']>0)|
        (df['players'].str.lower().str.contains('balogun')& df['ratings']>0)|
        (df['players'].str.lower().str.contains('nketiah')& df['ratings']>0)|
        (df['players'].str.lower().str.contains('martinelli')& df['ratings']>0)|
        (df['players'].str.lower().str.contains('nelson')& df['ratings']>0)]
        print(forwards)


        count=len(forwards)
        avg_frwd_ratings=sum(forwards['ratings'])/count
        print('AVERAGE FORWARDS RATING : ', avg_frwd_ratings)

  
goalkeeper=Gk()
goalkeeper.calculate_ratings()
    

defender=Def()
defender.calculate_ratings()

midfield=Mid()
midfield.calculate_ratings()

forwards=Attack()
forwards.calculate_ratings()
