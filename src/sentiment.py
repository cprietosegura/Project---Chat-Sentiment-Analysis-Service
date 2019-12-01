import nltk 
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
from bson.json_util import dumps

def getSentimentReport(chat):
    chat=json.loads(chat)
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
    print('--SENTIMENT REPORT--\n')
    print('The following conversation has been analyse using VADER \n')
    print(conversation)
    return df


