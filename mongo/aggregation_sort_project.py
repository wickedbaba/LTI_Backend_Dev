import datetime
import os
import pprint

from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient(MONGODB_URI)

db = client.bank

accounts_collection = db.accounts
conversion_rate_usd_to_gbp = 1.3

select_accounts = {"$match": {"account_type": "checking", "balance": {"$gt": 1500}}}

organize_by_original_balance = {"$sort": {"balance": -1}}

return_specified_fields = {
    "$project": {
        "account_type": 1,
        "balance": 1,
        "gbp_balance": {"$divide": ["$balance", conversion_rate_usd_to_gbp]},
        "_id": 0,
    }
}

pipeline = [
    select_accounts,
    organize_by_original_balance,
    return_specified_fields,
]

results = accounts_collection.aggregate(pipeline)



for item in results:
    pprint.pprint(item)

client.close()