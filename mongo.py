from pymongo import MongoClient
from pprint import pprint 

url = mongodb://localhost
client = MongoClient(url)
db = client.admin

serverStatusResult = db.command("serverStatus")
pprint(serverStatusResult)
