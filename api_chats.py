from bottle import route, run, get, post, request
from pymongo import MongoClient
from bson.json_util import dumps
import json
from mongo_populate import db, coll
import random
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
#from src.sentiment import getSentimentReport

#GET
@get("/")
def welcome():
    """you can get all the database content"""
    return "Welcome to the API! \n Enjoy exploring the chats."

@get("/<userName>")
def GetUserMessages(userName):
    """you can get all the user messages"""
    return dumps(coll.find({'userName':userName},{'userName':1,'text':1,'_id':0})) 

@get("/chat/<idChat>/list") 
def GetChats(idChat):
    """you can get all the messages of a selected chat"""
    return dumps(coll.find({'idChat' :int(idChat)},{'userName':1,'text':1,'_id':0}))

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


@get("/chat/<idChat>/sentiment") 
def sentimentReport(idChat):
    """Analyze messages from chat_id"""
    chat=dumps(coll.find({'idChat' :int(idChat)},{'userName':1,'text':1,'_id':0}))
    print(chat)
    print(chat[0])
    print(len(chat))
    report=getSentimentReport(chat)
    return report



#POST
@post('/user/create')
def newUser():
    """you can add an user to the database"""
    name = str(request.forms.get("userName"))
    print(name)
    new_id = coll.distinct("idUser")[-1] + 1
    print(new_id)
    new_user ={
        "idUser": new_id,
        "userName": name}
    print(new_user)
    coll.insert_one(new_user)
    print("User added to collection")


@post('/adduser')
def addUserProfile():
    """you can add an user and her message to the database"""
    idUser=coll.distinct("idUser")[-1] + 1
    name=str(request.forms.get("userName"))
    idMessage=coll.distinct("idMessage")[-1] + 1
    idChat=coll.distinct("idChat")[-1] + 1
    text=str(request.forms.get("text"))
    document={"idUser":idUser,
                "userName":name,
                "idMessage":idMessage,
                "idChat":idChat,
            
                "text":text}

    coll.insert_one(document)
    print("New user added to collection")



@post('/chat/<idChat>/adduser')
def addUserToChat(idChat):
    """you can add an user and her message to an existing chat"""
    idUser=coll.distinct("idUser")[-1] + 1
    name=str(request.forms.get("userName"))
    idMessage=coll.distinct("idMessage")[-1] + 1
    idChat=int(idChat)
    text=str(request.forms.get("text"))
    document={"idUser":idUser,
                "userName":name,
                "idMessage":idMessage,
                "idChat":idChat,
                "text":text}

    coll.insert_one(document)
    print("New user added to chat{}".format(idChat))


"""@post('/chat/<chat_id>/addmessage')
def addUserToChat(idChat,userName):
    #add message from an existing user to an existing chat
    idChat=int(idChat)
    name=str(userName)
    #averiguar cómo decirle que idUser corresponde al username indicado
    idUser=coll.distinct({'userName':name})
    idMessage=coll.distinct("idMessage")[-1] + 1
    text=str(request.forms.get("text"))
    document={"idUser":idUser,
                "userName":name,
                "idMessage":idMessage,
                "idChat":idChat,
                "text":text}

    coll.insert_one(document)
    print("New user added to chat{}".format(idChat))"""

     
run(host='0.0.0.0', port=8080)

