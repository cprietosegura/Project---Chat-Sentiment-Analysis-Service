import nltk 
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
from bson.json_util import dumps
import json


def getSentimentReport(chat):
    chat=json.loads(chat)
    sid = SentimentIntensityAnalyzer()
    scores={}
    for text in chat:
        scores['Message {} analysis'.format(chat.index(text)+1)]=(text['userName']+': '+text['text']),(sid.polarity_scores(text['text']))
    return scores


