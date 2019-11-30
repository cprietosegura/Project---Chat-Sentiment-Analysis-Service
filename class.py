from pymongo import MongoClient


class CollConection:

    def __init__(self,dbName,collection):
        self.client = MongoClient()
        self.db = self.client[dbName]
        self.collection=self.db[collection]

    def addDocument(self,document):
        a=self.collection.insert_one(document)
        print("Inserted", a.inserted_id)
        return a.inserted_id
    
    def addChat(self, idUser, name, idMessage, idChat, datetime, text):
        document={"idUser":idUser,
                "userName":name,
                "idMessage":idMessage,
                "idChat":idChat,
                "datetime":datetime,
                "text":text}
        return self.addDocument(document)

