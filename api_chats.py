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

@post('/adduser')
def addUser():
    idUser=coll.distinct("idUser")[-1] + 1
    name=str(request.forms.get("userName"))
    print('name')
    idMessage=coll.distinct("idMessage")[-1] + 1
    idChat=coll.distinct("idChat")[-1] + 1
    text=str(request.forms.get("text"))
    print('text')
    document={"idUser":idUser,
                "userName":name,
                "idMessage":idMessage,
                "idChat":idChat,
            
                "text":text}

    coll.insert_one(document)
    print("New user added to collection")

"""
@post('/user/create')

def newUser():
    name = str(request.forms.get("name"))
    new_id = coll.distinct("idUser")[-1] + 1
    new_user = {
        "idUser": new_id,
        "userName": name
    }
    coll.insert_one(new_user)
    print("User added to collection")
"""

     
run(host='0.0.0.0', port=8080)

