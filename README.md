
# Arsenal match prediction

Supporting Arsenal can be very challenging. One day they would perform very well and others not so much. Hence, I decided to use and apply machine learning to predict the upcoming matches results. There is a lot of variable that can determine the outcome of the match but for starter, this project predicts the results of upcoming matches based on the players recent forms (past 6 matches)
Datas were scraped from different websites and code were implement in OOP concept.

## Weekly prediction

Weekly prediction of matches will be updated at updated_weekly_prediction.ipynb notebook and at excel :
https://docs.google.com/spreadsheets/d/1cm8YsN_rHArOWOECN9V4z6SZLr6FEwodxyE7vOMAWY8/edit?usp=sharing


## Player sentiment analysis
Player sentiment analysis were also conducted where the data used are tweets related to players. The tweetes were gathered after matches to see the overall sentiment behind their performance post match. Tweets were retrieved using Twitter APIs and analysis were done in PowerBI. 
The analysis link :
https://app.powerbi.com/view?r=eyJrIjoiZjczZWZlNjYtNWU3NC00ODJmLTkzN2UtMTc2MDMwZWE5ZTBlIiwidCI6IjFmNTUxYWViLTdlYTEtNDcyYy05YWMwLTA5ZGU5YmYzMzA1MSIsImMiOjEwfQ%3D%3D&pageName=ReportSectionb5424e2e9bbc9b16576b





## Scripts description

| Scripts             | Description                                                              |
| ----------------- | ------------------------------------------------------------------ |
| main_scrape.py| scrape past performances of players for previous N number of matches|
| calculate_past_ratings.py | calculate past perforamnce of players for previous N number of matches based on players positions |
| scrape_predicted_lineups.py | scrape predicted lineups for upcoming match |
| calculate_predicted_lineups_pastperfomance.py | scrape predicted lineups past 6 match performances |
| weekly_ratings.py | scrape actual weekly player ratings after match |
| calculate_weekly_performance.py | calculate actual weekly player ratings after match based on players positions |
| EDA.ipynb | exploratory data analysis to find correlated variables that contributes to winning match |
| training_model.ipynb | train and testing different models to get best accuracy |
| updated_weekly_prediction.ipynb | weekly match results and scores prediction |



## Data gathering


Data were screped from :
- https://fbref.com/en/squads/18bb7c10/Arsenal-Stats
- https://www.whoscored.com/Teams/13/Show/England-Arsenal
- https://www.fantasyfootballscout.co.uk/team-news/


## Models

Diffrent classification models were used to predict binary classification and also multiouput classification. Training and testing models can be found at traing_model.ipynb notebook.

| Models             | Accuracy                                                              |
| ----------------- | ------------------------------------------------------------------ |
| Logistic regression with hyperparameter tuning | 100|
| Logistic regression | 75 |
| K Nearest Neighbour | 75 |
| Support Vector Machine | 75 |
| Random Forest | 50 |
| Gradient Boost | 50 |
| Ada Boost | 50 |
| XGradient Boost | 50| 


## What can be improved?

- Usage of real time data from the game at half time for more better predictions.
- Carry out sentiment analysis for future games from pundits and football analysers have more clarity of 

## License


[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)

