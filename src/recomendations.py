import requests
import nltk 
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity as distance
import numpy as np
import seaborn as sns

def getUserList(url):
    res=requests.get(url)
    users=res.json()
    lista_users=[]
    for u in users:
        lista_users.append(u['userName'])
    lista_users=list(set(lista_users))
    return lista_users

#url='http://localhost:8080/users'
#lista_users=getUserList(url)

def getUsersMessages(lista):
    all_usermess=[]
    for l in lista:
        url='http://localhost:8080/{}'.format(l)
        all_usermess.append(requests.get(url).json())
    return all_usermess

#all_usermess=getUsersMessages(lista_users)

def getUsMessages(username):
    userconv={}
    conv=""
    for user in username:
        conv+=user['text']
        userconv[user['userName']]=conv
    return userconv

"""todo=[]
for u in all_usermess:
    e=getUsMessages(u)
    todo.append(e)
dic_users={}
for dic in todo:
    keys=list(dic.keys())
    values=list(dic.values())
    dic_users[keys[0]]=values[0]"""
        
def recomendations(dic):
    count_vectorizer = CountVectorizer()
    sparse_matrix = count_vectorizer.fit_transform(dic.values())
    doc_term_matrix = sparse_matrix.todense()
    df = pd.DataFrame(doc_term_matrix, 
                    columns=count_vectorizer.get_feature_names(), 
                    index=dic.keys())
    similarity_matrix = distance(df, df)
    sim_df = pd.DataFrame(similarity_matrix, columns=dic.keys(), index=dic.keys())
    sns.heatmap(sim_df,annot=True)
    np.fill_diagonal(sim_df.values, 0)
    recomendations=sim_df.idxmax()
    return recomendations

#rec=recomendations(dic_users)
