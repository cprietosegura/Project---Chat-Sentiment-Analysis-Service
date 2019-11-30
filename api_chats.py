from bottle import route, run, get, post, request
from pymongo import MongoClient
from bson.json_util import dumps
from mongo_populate import db, coll
import random


@get("/")
def index():
    return dumps(coll.find())

@get("/chat/<userName>")
def GetUserMessages(userName):
    return dumps(coll.find({'userName':userName})) 

"""
@post('/adduser')
def addUser():
    idUser=collection.distinct("idUser")[-1] + 1
    name=request.forms.get("userName")
    idMessage=collection.distinct("idMessage")[-1] + 1
    idChat=collection.distinct("idChat")[-1] + 1
    datetime=request.forms.get("datetime")
    text=request.forms.get("text")
    document={"idUser":idUser,
                "userName":name,
                "idMessage":idMessage,
                "idChat":idChat,
                "datetime":datetime,
                "text":text}

    coll.insert_one(document)
    print("New user added to collection")

@post('/user/create')
def newUser():
    name = str(request.forms.get("name"))
    new_id = collection.distinct("idUser")[-1] + 1
    new_user = {
        "idUser": new_id,
        "userName": name
    }
    print(f"{name} added to collection with id {new_id}")"""


     
run(host='localhost', port=8080)

