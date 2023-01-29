import json
import subprocess
from pymongo import MongoClient
from pymongo import ASCENDING
from pymongo import DESCENDING
from pymongo import TEXT

# Take inputs of json file name and port number from the user
file_name = input("Enter a json file name (don't put extension): ")
port_number = input("Enter a port number: ")

# Loading or Opening the json file into the collection
import_command = "mongoimport --port " + port_number + " --db 291db --collection dblp --drop --numInsertionWorkers=10 --file " + file_name + ".json" 
import_command = import_command.split()
process = subprocess.Popen(import_command)
process.wait()

# Use client = MongoClient('mongodb://localhost:27017') for specific ports!
# Connect to the default port on localhost for the mongodb server.
client = MongoClient('mongodb://localhost:' + port_number)

# Create or open the document store database on server.
db = client["291db"]

# Create or open the collection in the db
collection = db["dblp"]

# create index for searching venues
collection.create_index([("references",1)])
collection.create_index([("venues",1)])

# creating a new field called year-text 
collection.update_many(
    {},
        [{
            "$set": { "year" : {'$toString': '$year'}}
        }]
)

# creating INDEX for searching authors and articles
# add case-insensitive option
collection.create_index(
    [("title" , TEXT),("authors", TEXT),  ("abstract" , TEXT),("venue" , TEXT), ("year" , TEXT) ],name="search_index",default_language='None')

list_of_collections = db.list_collection_names() 
if "Venues" in list_of_collections:
  db["Venues"].drop()

# create a materialized view for venues and numbers of their articles
def find_venues(): 
  collection.aggregate([
   { "$lookup":
      {
        "from": "dblp",
        "localField": "id",
        "foreignField": "references",
        "as": "joinResult"
      }
  }
  ,
    {
      
      "$unwind": {"path": "$joinResult","preserveNullAndEmptyArrays": True}
  },

  {
      "$group": {
        "_id":"$venue",
        "unique_id_list": {"$addToSet":"$joinResult.id"},
        "article_count" : {"$addToSet":"$id"}
      }
  }
  ,
  {"$project":{"venue":"$_id","_id":0,"rcount":{"$size":"$unique_id_list"},"article_count" : {"$size":"$article_count"}}}
  ,
  {
    "$match": {
      "venue": {"$ne":""}}
    }
  ,
  {"$sort": {"rcount":-1}}
  ,
  {"$merge": {"into":"Venues"}}
  ])

find_venues()












