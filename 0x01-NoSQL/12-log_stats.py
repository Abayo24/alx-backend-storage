#!/usr/bin/env python3
"""
script that provides some stats about Nginx logs stored in MongoDB
"""


from pymongo import MongoClient


def nginx_count():
    """provides some stats about Nginx logs stored in MongoDB"""
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    collection = db.nginx

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    
    """number of documents in nginx collection"""
    docs_count = collection.count_documents({})
    print(f'{docs_count} logs')

    """number of documents with specific method"""
    print('Methods:')
    for method in methods:
        method_count = collection.count_documents({"method": method})
        print(f'\tmethod {method}: {method_count}')

    getStatus_count = collection.count_documents({"method": "GET", "path": "/status"})
    print(f'{getStatus_count} status check')

if __name__ == "__main__":
    nginx_count()
