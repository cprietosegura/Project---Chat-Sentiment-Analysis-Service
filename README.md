# Project---Chat-Sentiment-Analysis-Service
En este proyecto he desarrollado una API en Python conectada a una base de datos en MongoDB Atlas con chats y conversaciones de diferentes usuarios. La API, desarrollada con Bottle, ofrece un servicio de consulta de dichos chats y usuarios, así como la posibilidad de obtener un informe de sentimientos de cada chat. Asimismo, también es posible cargar nuevos usuarios y conversaciones a la base de datos existente.

### Cómo usar la API: ###

- (GET) "/users"

        Propósito: Muestra todos los usuarios de la base de datos
        Params: no necesita
        Returns: usernames
    
- (GET) "/userName"

        Propósito: Muestra todos los mensajes de un usuario
        Params: userName
        Returns: text y username

- (GET) "/chat/idChat/list"

        Propósito: Muestra todos los mensajes de un chat
        Params: idChat
        Returns: text y username del chat
    
- (GET) "/chat/idChat/sentiment"

        Propósito: Mostrar un análisis de sentimiento de un chat
        Params: idChat
        Returns: El score de cada mensaje con su username, una media final de los sentimientos del chat.

- (POST) "/user/create"

        Propósito: Crear un nuevo usuario en la base de datos. 
        Params: userName y su text

- (POST) "/chat/idChat/add"

        Propósito: Incorporar contenido a un chat. Ofrece la posibilidad de que el chat exista ya o de que sea nuevo. Se pueden añadir participantes con nuevos mensajes, o únicamente mensajes de usuarios que ya están en la conversación.  
        Params: idChat, userName y su text


### Documentos ###

El archivo api_chat.py es el fichero principal del proyecto, desde el que corre la API a través del módulo Bottle en un entorno local.

En mongo_populate.py se establece la connexión con la base de datos y se carga el json con el contenido.

En Requests_api.ipynb se pueden encontrar algunos ejemplos de las requests que se pueden hacer a la API.

En la carpeta Input se encuentra la base de datos original que se cargó en MongoDB Atlas.

En la carpeta src contiente el fichero sentiment.py que aloja las funciones para la funcionalidad de la API que permite hacer el análisis de sentimiento.

En requirements.txt hay una lista con todas las instancias que se han utilizado para el proyecto.

Finalmente, en la carpeta in_process se hayan varios ficheros en los que todavía se está desarrollando una nueva funcionalidad de la api para recomendar usuarios que se implementará en el futuro.
