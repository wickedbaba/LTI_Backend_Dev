import datetime
import os
import pprint

from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient(MONGODB_URI)


db = client.bank

accounts_collection = db.accounts

select_by_balance = {"$match": {"balance":{"$lt":1000}}}

select_by_avg = {
    "$group": {
        "_id":"$account_type",
        "avg_balance":{"$avg":"balance"}
    }
}

pipeline  =[select_by_balance,select_by_avg]

result = accounts_collection.aggregate(pipeline)

for item in result:
    pprint.pprint(item)


client.close()


