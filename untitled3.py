# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 16:36:09 2023

@author: praveen
"""

from flask import Flask
app = Flask(__name__)

import nltk
nltk.download('punkt')

@app.route('/data')
def tasks():
    return apiResponse

# pip install vaderSentiment

# import SentimentIntensityAnalyzer class
# from vaderSentiment.vaderSentiment module.
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# function to print sentiments
# of the sentence.
def sentiment_scores(sentence):

	# Create a SentimentIntensityAnalyzer object.
	sid_obj = SentimentIntensityAnalyzer()

	# polarity_scores method of SentimentIntensityAnalyzer
	# object gives a sentiment dictionary.
	# which contains pos, neg, neu, and compound scores.
	sentiment_dict = sid_obj.polarity_scores(sentence)
	return sentiment_dict['compound']
	
from newspaper import Article


def getCategory(score):

	# decide sentiment as positive, negative and neutral
	if score >= 0.05 :
		return ("Positive")

	elif score <= - 0.05 :
		return ("Negative")

	else :
		return ("Neutral")
    
def getSummaryFromLink(url):
    articleData = Article(url, language="en")
    articleData.download()
 
    #To parse the article
    articleData.parse()
 
    #To perform natural language processing ie..nlp
    articleData.nlp()
 
    #To extract title
    print("Article's Title:")
    print(articleData.title)
    print("n")
     
    #To extract text
    print("Article's Text:")
    print(articleData.text)
    print("n")
     
    #To extract summary
    print("Article's Summary:")
    print(articleData.summary)
    print("n")
     
    #To extract keywords
    print("Article's Keywords:")
    print(articleData.keywords)
    
    return articleData

from transformers import pipeline
summarizer = pipeline("summarization")

def getSummaryFromText(text):
    summary_text = summarizer(text, max_length=100, min_length=5, do_sample=False)[0]['summary_text']
    return summary_text

#positive sentiment : (compound score >= 0.05) 
#neutral sentiment : (compound score > -0.05) and (compound score < 0.05) 
#negative sentiment : (compound score <= -0.05)

import feedparser
import pandas as pd

NewsFeed = feedparser.parse("https://timesofindia.indiatimes.com/rssfeedstopstories.cms")
#NewsFeed = feedparser.parse("https://feeds.feedburner.com/ndtvnews-top-stories")
#NewsFeed2 = feedparser.parse("https://www.indiatoday.in/rss/home")
#NewsFeed.append
numberOfPosts = len(NewsFeed.entries)
print ('Number of RSS posts :', numberOfPosts)


temp_val = []
dataset = pd.DataFrame(columns=['title', 'summary', 'sentiment','score'])
for i in range (0,numberOfPosts):
    entry = NewsFeed.entries[i]
    print ('Post Title :',entry.title)
    print ('Post Summary :',entry.summary)
   
    if len(entry.summary) > 0 :
        compound_val = sentiment_scores(entry.summary)
        
    else :
        articleSummary = getSummaryFromLink(entry.link).summary
        entry.summary = getSummaryFromText(articleSummary)
        compound_val = sentiment_scores(entry.summary)
    temp_val = []
    temp_val.append([entry.title, entry.summary, getCategory(compound_val), compound_val])
    temp_df = pd.DataFrame(temp_val, columns=['title', 'summary', 'sentiment','score'])
    dataset = dataset.append(temp_df, ignore_index=True)
    
dataset.to_csv('reportVader.csv')
apiResponse = dataset.to_json(orient='records', force_ascii=False)
print("finished..........")
if __name__ == "__main__":
    app.run(debug=True)