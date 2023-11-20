from pymongo import MongoClient
from collections import Counter


def get_mongodb():
    client = MongoClient("mongodb://localhost")   
    db = client.hw_10
    return db

def save_tag_to_quote(quote, tags):
    db = get_mongodb()
    quote = db.quotes.find_one({"quote": quote})
    for tag in tags:
        tag = db.tags.find_one({"name": tag})
        db.tag_to_quote.insert_one({'id_quote': quote["_id"], 'id_tag': tag["_id"] })
        
def top_ten_tags():
    db = get_mongodb()
    tag_to_quote= db.tag_to_quote.find()
    list_tag = [a['id_tag'] for a in tag_to_quote]
    top_ten = Counter(list_tag).most_common(10)
    return {db.tags.find_one({"_id": tag[0]})["name"]: index for index,tag in enumerate(top_ten)}
