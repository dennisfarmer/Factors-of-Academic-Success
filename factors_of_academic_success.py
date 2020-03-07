"""
Created on Sat Feb 22 12:44:24 2020

@author: Dennis
"""
import pandas as pd
import re # regex module
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns

# Read survey spreadsheets
filepath = "C:/Users/Dennis/Documents/Git/Factors of Academic Success/Survey Spreadsheets/"

survey101 = pd.read_excel(filepath + "Factors of Academic Success Survey (1.01).xlsx")
survey202 = pd.read_excel(filepath + "Factors of Academic Success Survey (2.02).xlsx")

# Merge dataframes
surveydata = pd.merge(left=survey101, right=survey202, how="outer")
surveydata.columns = map(str.lower, surveydata.columns)

# Drop columns that I've decided to not use in analysis
surveydata = surveydata.drop(['hobby', 'tv_laugh_track', 'perfectionist', 'large_ego', 'good_at_comedy'], axis=1)

##########################################
# Basic data cleaning and transformation #
##########################################

# Convert list cells to lists
select_columns = ['self_improv', 'activities', 'watched_media', 'chosen_music_artists']
surveydata[select_columns]= surveydata[select_columns].apply(lambda x: x.str.split(","))
    
### Calculate the average amount of sleep for each person
def time_to_datetime(column, dataf=surveydata):
    # Insert Date
    time_day = []
    for i in range(dataf.shape[0]):
        if column == 'up_from_bed' or (column == 'go_to_bed' and dataf[column][i].hour < 5): 
            time_day.append("2000/01/02 ") # Special for timedelta where one column can have more than one possible day
        else:
            time_day.append("2000/01/01 ")
        
    # Concat date and time and convert to datetime object    
    return (pd.Series(time_day) + dataf[column].astype(str)).apply(lambda x: dt.datetime.strptime(x, "%Y/%m/%d %H:%M:%S"))
    
surveydata.insert(22, 'avg_sleep_hours', time_to_datetime('up_from_bed') - time_to_datetime('go_to_bed'))

def clean_avg_sleep(hours_of_sleep):
    if hours_of_sleep > 15:
        return hours_of_sleep - 12
    else:
        return hours_of_sleep
    
surveydata.avg_sleep_hours = surveydata.avg_sleep_hours.apply(lambda x: clean_avg_sleep(x.seconds / 3600))

### Map all music majors to be called "Music"
surveydata.loc[surveydata.major.str.contains(r"music", case=False, na=False, regex=True), 'major'] = "Music"

### Compare SAT and ACT scores and keep the highest one as a converted SAT score
act_sat = {'36':1590, '35':1540, '34':1500, '33':1460, '32':1430, '31':1400, '30':1370, '29':1340, '28':1310, '27':1280, '26':1240, '25':1210, '24':1180, '23':1140, '22':1110, '21':1080, '20':1040, '19':1010, '18':970}
def act_to_sat(act):
    if np.isnan(act):
        return np.NaN
    else:
        score = str(int(act))
        if score in act_sat:
            return act_sat[score]
        else:
            return np.NaN
        
surveydata.insert(11, 'converted_sat', surveydata.act.apply(act_to_sat))
select_rows = (surveydata.sat.fillna(0) > surveydata.converted_sat.fillna(0))
surveydata.loc[select_rows, 'converted_sat'] = surveydata.loc[select_rows, 'sat']
surveydata.converted_sat = surveydata.converted_sat.fillna(0).astype(int)

### Clean Myers-Briggs types to capitalize and place letters in correct order
def clean_myers_briggs(mbti):
    try:
        mbti = mbti.upper()
    except AttributeError:
        return np.NaN
    return re.findall(r'E|I', mbti)[0] + re.findall(r'S|N', mbti)[0] + re.findall(r'T|F', mbti)[0] + re.findall(r'P|J', mbti)[0]
    
surveydata.myers_briggs = surveydata.myers_briggs.apply(clean_myers_briggs)

### Convert first 36 big5 personality score rows to range 1-5 (from range 1-10)
def clean_big5(score):
    score = score//2
    if score == 0:
        return score + 1
    return score

select_columns = ['openness', 'conscientiousness', 'extraversion', 'agreeableness', 'neuroticism']
big5_rows = surveydata.iloc[:35][select_columns].applymap(clean_big5)
surveydata.iloc[:35][select_columns] = big5_rows



#avg_sleep_per_grade = surveydata.pivot_table(values='avg_sleep_hours', index='school_year', aggfunc= np.mean)
     
#pv_scores = surveydata.pivot_table(values='avg_sleep_hours', index='converted_sat', aggfunc=np.mean, margins=True)
#pv_scores.plot(kind='barh', xlim=(0,15), title='Mean Hours of Sleep by SAT Score', legend=False)
#plt.show
        
        
        
        
        
        
        



### (Big brain project) Use Classes and shit to convert Big5 personality dimensions to Myers Briggs personalities
#https://www.reddit.com/r/mbti/comments/6ubauu/big_five_and_mbti_correlationstheory/
#https://personalityjunkie.com/09/openness-myers-briggs-mbti-intuition-big-five-iq-correlations/

#surveydata_personalities = surveydata[['timestamp', 'myers_briggs', 'openness', 'conscientiousness', 'extraversion', 'agreeableness', 'neuroticism']]
#
#class MyerBrigg:
#    def __init__(self, big5):
#        self.o = big5[0] #openness
#        self.c = big5[1] #conscientiousness
#        self.e = big5[2] #extraversion
#        self.a = big5[3] #agreeableness
#        self.n = big5[4] #neuroticism
#    
#    def crude_myerbrigg_type(self): #I'm not a psych major, I just really like brains
#        if self.e > 5:              
#            self.IntroExtra = 'E'
#    
    
    



####################
# Data Exploration #
####################

#number of clubs could lead to better grades
#what percentage of band nerds are religious?

#surveydata.to_excel("SurveyData")


    
#fig, axes = plt.subplots()



