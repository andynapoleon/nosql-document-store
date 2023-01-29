from pymongo import MongoClient

# Use client = MongoClient('mongodb://localhost:27017') for specific ports!
# Connect to the default port on localhost for the mongodb server.
port_number = input("Enter the port number: ")
client = MongoClient('mongodb://localhost:' + port_number)

# Create or open the document store database on server.
db = client["291db"]
collection = db["dblp"]
venues = db["Venues"]

# 1 - FUNCTIONS for searching for articles
#ar_search = "\"Makoto\" \"Sato\""

def find_articles(keywords):        
  keywords = keywords.split()
  ar_result = collection.find({"$text":{"$search": '\"' + '\" \"'.join(keywords) + '\"'
  , "$caseSensitive": False, "$diacriticSensitive": False}})
  return ar_result


def find_references(aid):
  ref_result = collection.find({"references": aid})
  return ref_result

# 2 - FUNCTIONS for searching for authors only one keyword inputted for searching for authors
#au_search = "Hussein"

def find_authors(keyword):
  au_result = collection.aggregate([
    {"$match":{"$text":{"$search": keyword, "$caseSensitive": False, "$diacriticSensitive": False}}},
    {"$unwind": "$authors"},
    {"$match": {"authors" : {"$regex" : "\\b" + keyword + "\\b", "$options": 'i'}}},
    {"$group": {"_id": "$authors", "count": {"$sum": 1}}}
  ])
  return au_result

def find_article_based_on_authors(name):
  result = collection.aggregate([
    {"$match": {"authors": name}},
    {"$sort": {"year":-1}}
  ])
  return result

# 3 - FUNCTIONS for listing the venues
def find_top_venues(n):
  top_venues = venues.find().limit(n)
  return top_venues

# 4 - FUNCTIONS for adding an article
# check if id already exists in the database
def check_exists(aid):
  exist = len(list(collection.find({"id": aid})))
  return exist

# create new data (article)
def create_new_article(aid,title,authors,year):
  new_article = {
  "abstract" : "",
  "authors" : authors,
  "n_citations" : 0,
  "references" : [],
  "title" : title,
  "venue" : "",
  "id" : aid,
  "year" : year
  }
  return new_article

# add article if not exists
def add_article(aid,title,authors,year):
  new_article = create_new_article(aid,title,authors,year)
  collection.insert_one(new_article)

  
