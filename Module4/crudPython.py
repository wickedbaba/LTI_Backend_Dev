import datetime
import os
import pprint

from pymongo import MongoClient
from bson.objectid import ObjectId


client = MongoClient(MONGODB_URI)


db = client.bank

accounts_collection = db.accounts


# ----------------------------------------------------------------------------------------------------------------------------
# example of insert one

new_account = {
    "account_holder": "Linus Torvalds",
    "account_id": "MDB829001337",
    "account_type": "checking",
    "balance": 50352434,
    "last_updated": datetime.datetime.utcnow(),
}
result = accounts_collection.insert_one(new_account)

document_id = result.inserted_id
print(f"_id of inserted document: {document_id}")

# ----------------------------------------------------------------------------------------------------------------------------
# example of insert many

new_accounts = [
    {
        "account_id": "MDB011235813",
        "account_holder": "Ada Lovelace",
        "account_type": "checking",
        "balance": 60218,
    },
    {
        "account_id": "MDB829000001",
        "account_holder": "Muhammad ibn Musa al-Khwarizmi",
        "account_type": "savings",
        "balance": 267914296,
    },
]

result = accounts_collection.insert_many(new_accounts)
document_id = result.inserted_ids
print(document_id, result)

client.close()
# ----------------------------------------------------------------------------------------------------------------------------
# finding an element ->  find_one() and find()

document_to_find = {"balance":{"$gt":4700}}

cursor = accounts_collection.find(document_to_find)

num_docs = 0

for document in cursor:
    pprint.pprint(document)
    print()
    num_docs+=1

print(num_docs)



client.close()

# ----------------------------------------------------------------------------------------------------------------------------
# updating an element ->  update_one() and update_many()

document_to_update = {"_id": ObjectId("62d6e04ecab6d8e130497482")}

add_to_balance = {"$inc": {"balance": 100}}

result = accounts_collection.update_one(document_to_update, add_to_balance)
print("Documents updated: " + str(result.modified_count))

pprint.pprint(accounts_collection.find_one(document_to_update))

# update many -> 

select_accounts = {"account_type": "savings"}

# Update
set_field = {"$set": {"minimum_balance": 100}}

# Write an expression that adds a 'minimum_balance' field to each savings acccount and sets its value to 100.
result = accounts_collection.update_many(select_accounts, set_field)

print("Documents matched: " + str(result.matched_count))
print("Documents updated: " + str(result.modified_count))
pprint.pprint(accounts_collection.find_one(select_accounts))

client.close()

# ----------------------------------------------------------------------------------------------------------------------------
# deleting an element -> delete_one() and delete_many()

