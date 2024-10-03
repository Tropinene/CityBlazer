import json
import os
from pymongo import MongoClient
from dotenv import load_dotenv


def parse_geojson(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Extract 'name', 'state', and 'coordinates'
    result = []
    for feature in data['features']:
        name = feature['properties'].get('name', '')
        state = feature['properties'].get('state', '')
        coordinates = feature['geometry'].get('coordinates', [])
        result.append({
            "name": name,
            "state": state,
            "coordinates": coordinates
        })
    return result


# Function to insert data into MongoDB
def insert_into_mongodb(data, db_name='US_cities', collection_name='map'):
    load_dotenv()
    mongo_uri = os.getenv('MONGO_URI')
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    # Insert data into MongoDB collection
    if data:
        collection.insert_many(data)
        print(f"Inserted {len(data)} records into the MongoDB collection.")
    else:
        print("No data to insert.")


# Function to process all GeoJSON files in a folder
def process_geojson_folder(folder_path):
    # Loop through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".geo.json"):  # Only process GeoJSON files
            file_path = os.path.join(folder_path, filename)
            print(f"Processing file: {file_path}")

            # Extract data and insert into MongoDB
            geo_data = parse_geojson(file_path)
            insert_into_mongodb(geo_data)


def main():
    states_abbreviations = [
        'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
        'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
        'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
        'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
        'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY',
        'PR'
    ]
    # Folder path to your GeoJSON files (AK folder)
    for i in states_abbreviations:
        folder_path = '/Users/yyy/Desktop/USA/' + i + '/'

        # Process all files in the folder and insert into MongoDB
        process_geojson_folder(folder_path)

        print("All files processed and data inserted successfully into MongoDB.")
        print("--------------------------------[*]--------------------------------")


if __name__ == "__main__":
    main()
