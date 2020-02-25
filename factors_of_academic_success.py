"""
Created on Sat Feb 22 12:44:24 2020

@author: Dennis
"""
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns

# Read survey spreadsheets
#filepath = "C:/Users/Dennis/Documents/Factors of Academic Success/"
filepath = "C:/Users/Dennis/Documents/Git/Factors of Academic Success/Survey Spreadsheets/"

survey101 = pd.read_excel(filepath + "Factors of Academic Success Survey (1.01).xlsx")

# Merge dataframes
survey101 = survey101.loc[:,"TIMESTAMP":"GOOD_AT_COMEDY"]
#surveydata = pd.merge(left=survey101, right=othersurvey, how="left") or maybe concat, idk lol
surveydata = survey101

##########################################
# Basic data cleaning and transformation #
##########################################

# Convert list cells to lists
for column in ["SELF_IMPROV", "ACTIVITIES", "WATCHED_MEDIA", "CHOSEN_MUSIC_ARTISTS"]:
    surveydata[column] = surveydata[column].str.split(",")
    
### Calculate the average amount of sleep for each person
def time_to_datetime(column, dataf=surveydata):
    time_day = []
    time_time = []
    time_dt = []
    # Insert Date
    for i in range(dataf.shape[0]):
        if column == "UP_FROM_BED" or (column == "GO_TO_BED" and dataf[column][i].hour < 5): # Special for timedelta where one column can have more than one possible day
            time_day.append("2000/01/02 ")
        else:
            time_day.append("2000/01/01 ")
        
    # Insert Time        
    for time in list(dataf[column]):
        time_time.append(str(time))
    
    # Concat date and time and convert to datetime object
    for date_time in list(pd.Series(time_day) + pd.Series(time_time)):
        time_dt.append(dt.datetime.strptime((date_time), "%Y/%m/%d %H:%M:%S"))
    
    return pd.Series(time_dt)
    
surveydata.insert(24, "AVG_SLEEP_HOURS", time_to_datetime("UP_FROM_BED") - time_to_datetime("GO_TO_BED"))

def clean_avg_sleep(hours_of_sleep):
    if hours_of_sleep > 15:
        return hours_of_sleep - 12
    else:
        return hours_of_sleep
    
surveydata["AVG_SLEEP_HOURS"] = surveydata["AVG_SLEEP_HOURS"].apply(lambda x: x.seconds / 3600).apply(clean_avg_sleep)

### Map all music majors to be called "Music"
surveydata.loc[surveydata["MAJOR"].str.contains(r"music", case=False, na=False, regex=True), "MAJOR"] = "Music"
#surveydata[musicselect]["MAJOR"] = "Music" # <-- Raises SettingWithCopyWarning

### Compare SAT and ACT scores and keep the highest one as a converted SAT score



### (Big brain project) Use Classes and shit to convert Big5 personality dimensions to Myers Briggs personalities
#https://www.reddit.com/r/mbti/comments/6ubauu/big_five_and_mbti_correlationstheory/
#https://personalityjunkie.com/09/openness-myers-briggs-mbti-intuition-big-five-iq-correlations/

surveydata_personalities = surveydata[["TIMESTAMP", "MYERS_BRIGGS", "OPENNESS", "CONSCIENTIOUSNESS", "EXTRAVERSION", "AGREEABLENESS", "NEUROTICISM"]]

#number of clubs could lead to better grades
#what percentage of band nerds are religeous?



####################
# Data Exploration #
####################


#surveydata.to_excel("SurveyData")


    
#fig, axes = plt.subplots()



