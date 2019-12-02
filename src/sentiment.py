import nltk 
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
from bson.json_util import dumps
import json


def getFinalMetric(chat):
    """performs the mean of all messages in chat an returns the final metric"""
    sid = SentimentIntensityAnalyzer()
    scores=[]
    conversation=[]
    for text in chat:
        conversation.append(text['userName']+': '+text['text'])
        scores.append(sid.polarity_scores(text['text']))
    df=pd.DataFrame(scores)
    df=df[['neg', 'neu', 'pos']]
    df=df.rename(columns={'neg':'Negative', 'neu':'Neutral', 'pos':'Positive'})
    means=df.mean(axis = 0) 
    df=pd.DataFrame(means)
    df.columns = ['Scores']
    df.index.name= 'Sentiment Metric'
    scores=df['Scores']
    final_sentiment_metric={}
    for s in scores:
        final_sentiment_metric['Negative']=scores[0]
        final_sentiment_metric['Positive']=scores[1]
        final_sentiment_metric['Neutral']=scores[2]
    return final_sentiment_metric


def getSentimentReport(chat):
    """creates a report with the score of all messages and adds the final metric"""
    chat=json.loads(chat)
    sid = SentimentIntensityAnalyzer()
    scores={}
    for text in chat:
        scores['Message {} analysis'.format(chat.index(text)+1)]=(text['userName']+': '+text['text']),(sid.polarity_scores(text['text']))
    scores['Complete chat sentiment Metric']=getFinalMetric(chat)    
    return scores


