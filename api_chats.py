from bottle import route, run, get, post, request
from pymongo import MongoClient
from bson.json_util import dumps
from mongo_populate import db, coll
import random
from src.sentiment import getSentimentReport, getFinalMetric
from src.recomendations import getUserList, getUsersMessages,getUsMessages,recomendations

#GET
@get("/")
def welcome():
    """gives a welcome message"""
    return "Welcome to the Chats API! \n Enjoy exploring the chats, adding new users and messages and analyzing their sentiment metric."

@get("/<userName>")
def GetUserMessages(userName):
    """Returns all the user messages"""
    return dumps(coll.find({'userName':userName},{'userName':1,'text':1,'_id':0}))

@get("/users")
def getAllUsers():
    """Returns all users"""
    return dumps(coll.find({},{'userName':1,'_id':0}))      

@get("/chat/<idChat>/list") 
def getUsers(idChat):
    """Returns all the messages of a selected chat"""
    return dumps(coll.find({'idChat' :int(idChat)},{'userName':1,'text':1,'_id':0}))

@get("/chat/<idChat>/sentiment") 
def sentimentReport(idChat):
    """Returns a report with the sentiment metric from a chat_id"""
    chat=dumps(coll.find({'idChat' :int(idChat)},{'userName':1,'text':1,'_id':0}))
    report=getSentimentReport(chat)
    return report

@get("/user/<userName>/recommend")
def GetUserMessages(userName):
    """Returns all the user messages"""
    url='http://localhost:8080/users'
    lista_users=getUserList(url)
    all_usermess=getUsersMessages(lista_users)
    todo=[]
    for u in all_usermess:
        e=getUsMessages(u)
        todo.append(e)
    dic_users={}
    for dic in todo:
        keys=list(dic.keys())
        values=list(dic.values())
        dic_users[keys[0]]=values[0]

    rec=recomendations(dic_users)
    dic={}
    dic['recomendation']=rec.loc[userName]
    return dumps(dic)



#POST
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


@post('/chat/<idChat>/add')
def addUserToChat(idChat):
    """Adds user and messages to a chat"""

    idUser=coll.distinct("idUser")[-1] + 1
    name=str(request.forms.get("userName"))
    idMessage=coll.distinct("idMessage")[-1] + 1
    idChat=int(idChat)
    text=str(request.forms.get("text"))
    lista=list(coll.find({}))
    for l in lista:
        if l['userName']==name:
            idUser = l['idUser']
            
    document={"idUser":idUser,
                "userName":name,
                "idMessage":idMessage,
                "idChat":idChat,
                "text":text}
    coll.insert_one(document)
    print("New user added to chat{}".format(idChat))
     
run(host='0.0.0.0', port=8080)

