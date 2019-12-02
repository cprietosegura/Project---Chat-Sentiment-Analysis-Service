from bottle import route, run, get, post, request
from pymongo import MongoClient
from bson.json_util import dumps
from mongo_populate import db, coll
import random
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
#import pandas as pd
from src.sentiment import getSentimentReport, getFinalMetric

#GET
@get("/")
def welcome():
    """gives a welcome message"""
    return "Welcome to the Chats API! \n Enjoy exploring the chats, adding new users and messages and analyzing their sentiment metric."

@get("/<userName>")
def GetUserMessages(userName):
    """Returns all the user messages"""
    return dumps(coll.find({'userName':userName},{'userName':1,'text':1,'_id':0})) 

@get("/chat/<idChat>/list") 
def GetChats(idChat):
    """Returns all the messages of a selected chat"""
    return dumps(coll.find({'idChat' :int(idChat)},{'userName':1,'text':1,'_id':0}))

@get("/chat/<idChat>/sentiment") 
def sentimentReport(idChat):
    """Returns a report with the sentiment metric from a chat_id"""
    chat=dumps(coll.find({'idChat' :int(idChat)},{'userName':1,'text':1,'_id':0}))
    print(chat)
    print(chat[0])
    print(len(chat))
    report=getSentimentReport(chat)
    return report


#POST
"""@post('/user/create')
def newUser():
    #Adds a new user to the database
    name = str(request.forms.get("userName"))
    new_id = coll.distinct("idUser")[-1] + 1
    new_user ={
        "idUser": new_id,
        "userName": name}
    all_users = list(coll.aggregate([{'$project':{'userName':1}}]))
    if name in [user['userName'] for user in all_users]:
        print("Error! This user already exists.")
    else:
        coll.insert_one(new_user)
        print("User added to collection")"""


@post('/user/create')
def addUserProfile():
    """Adds new user and her message to new chat in the database"""
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
    all_users = list(coll.aggregate([{'$project':{'userName':1}}]))
    if name in [user['userName'] for user in all_users]:
        print("Error! This user already exists.")
    else:
        coll.insert_one(document)
        print("User and message added to collection")


@post('/chat/<idChat>/adduser')
def addUserToChat(idChat):
    """you can add an user and her message to an existing chat"""
    #que busque si existe el usuario y que use su id si existe
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
    print("New user and message added to chat{}".format(idChat))"""

     
run(host='0.0.0.0', port=8080)

