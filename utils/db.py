from pymongo import MongoClient
from dotenv import load_dotenv
import os


def connect_to_mongodb():
    load_dotenv()
    mongo_uri = os.getenv('MONGO_URI')
    client = MongoClient(mongo_uri)

    db = client['US_cities']
    collection = db['map']

    first_doc = collection.find_one()
    if first_doc:
        print("Successfully connected to MongoDB. First document in 'map' collection:")
        print(first_doc)
    else:
        print("Connected to MongoDB but the 'map' collection is empty or does not exist.")

    return collection


if __name__ == "__main__":
    map_collection = connect_to_mongodb()
