# networksecurity/push_data.py
import os
import sys
import json
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logger.logger import logger   # <-- use the logger object

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
if not MONGO_DB_URL:
    raise ValueError("MONGO_DB_URL environment variable is not set")

import certifi
import pymongo
import pandas as pd


class NetworkDataExtract:
    def __init__(self):
        pass   # nothing to raise here

    def csv_to_json_convertor(self, file_path: str):
        try:
            df = pd.read_csv(file_path)
            df.reset_index(drop=True, inplace=True)
            records = list(json.loads(df.T.to_json()).values())
            return records
        except Exception as e:
            logger.exception("CSV → JSON conversion failed")
            raise NetworkSecurityException(e, sys) from e

    def insert_data_mongodb(self, records, database, collection):
        try:
            client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=certifi.where())
            db = client[database]
            coll = db[collection]
            inserted = coll.insert_many(records).inserted_ids
            client.close()
            return len(inserted)
        except Exception as e:
            logger.exception("MongoDB insert failed")
            raise NetworkSecurityException(e, sys) from e


if __name__ == "__main__":
    # Use pathlib → OS-independent
    ROOT = Path(__file__).resolve().parents[1]      # project root
    FILE_PATH = "C:\Users\15007010\Desktop\Network Security\Network_Data\phisingData.csv" 
    DATABASE = "KRISHAI"
    COLLECTION = "NetworkData"

    extractor = NetworkDataExtract()
    records = extractor.csv_to_json_convertor(str(FILE_PATH))
    logger.info(f"Converted {len(records)} rows to JSON")

    n = extractor.insert_data_mongodb(records, DATABASE, COLLECTION)
    logger.info(f"Inserted {n} documents into MongoDB")
    print(n)

    