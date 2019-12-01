from bottle import route, run, get, post, request
from pymongo import MongoClient
from bson.json_util import dumps
from mongo_populate import db, coll
import random

#GET
@get("/")
def index():
    """you can get all the database content"""
    return dumps(coll.find())

@get("/<userName>")
def GetUserMessages(userName):
    """you can get all the user messages"""
    return dumps(coll.find({'userName':userName},{'userName':1,'text':1,'_id':0})) 

@get("/chat/<idChat>/list") 
def GetChats(idChat):
    """you can get all the messages of a selected chat"""
    return dumps(coll.find({'idChat' :int(idChat)},{'userName':1,'text':1,'_id':0}))


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





     
run(host='0.0.0.0', port=8080)

