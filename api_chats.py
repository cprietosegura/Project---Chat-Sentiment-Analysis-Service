from bottle import route, run, get, post, request
import random
from mongo import CollConection
import bson
import getpass



@get("/chat/<tipo>")
def demo2(tipo):
    print(f"un chiste de {tipo}")
    if tipo == "chiquito":
        return {
            "chiste": "Van dos soldados en una moto y no se cae ninguno porque van soldados"
        }
    elif tipo == "eugenio":
        return {
            "chiste": "Saben aquell que diu...."
        }
    else:
        return {
            "chiste": "No puedorrr!!"
        }

@post('/add')
def add():
    print(dict(request.forms))
    idUser=request.forms.get("idUser")
    name=request.forms.get("userName")
    idMessage=request.forms.get("idMessage")
    idChat=request.forms.get("idChat")
    datetime=request.forms.get("datetime")
    text=request.forms.get("text")

    return {
        "inserted_doc": str(coll.addChat(idUser, name, idMessage, idChat, datetime, text))}


password = getpass.getpass("Insert your AtlasMongoDB admin_1019 password: ")
connection = "mongodb+srv://Celia_Mongodb:{}@cluster0-u6tdq.mongodb.net/test?retryWrites=true&w=majority".format(password)

coll=CollConection('chats-sentiment','chat1')
run(host='0.0.0.0', port=8080)

