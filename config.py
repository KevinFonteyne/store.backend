import pymongo
import certifi 

con_str = "mongodb+srv://cynderkyn:bankaiboi226@c2.pssh1uw.mongodb.net/?retryWrites=true&w=majority"


client = pymongo.MongoClient(con_str, tlsCAFile=certifi.where())

db = client.get_database("TechJunkies")