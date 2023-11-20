import json
from bson.objectid import ObjectId

from pymongo import MongoClient
from collections import Counter
client = MongoClient("mongodb://localhost")

db = client.hw_10

#Создание БД authors
with open("authors.json", 'r', encoding = 'utf=8') as fd:
    authors = json.load(fd)
    for author in authors:
        db.authors.insert_one({
            'fullname': author['fullname'],
            'born_date': author['born_date'],
            'born_location': author['born_location'],
            'description' : author['description'],
        })

#Создание БД quotes и tags
with open("quotes.json", 'r', encoding = 'utf=8') as fd:
    quotes = json.load(fd)
    tags = set()
    for quote in quotes:
        author = db.authors.find_one({'fullname': quote['author']})
        if author:
            db.quotes.insert_one({
                'quote': quote['quote'],
                'tags': quote['tags'],
                'author': ObjectId(author['_id'])
                })   
        for tag in quote['tags']:
            tags.add(tag)          
    db.tags.insert_many([{"name": tag} for tag in tags])

#Создание БД tag_to_quote 
for tag in db.tags.find():
    for quote in db.quotes.find({'tags':tag['name']}):
        db.tag_to_quote.insert_one({'id_quote': quote["_id"], 'id_tag': tag["_id"] })
        


