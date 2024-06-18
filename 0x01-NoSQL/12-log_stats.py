#!/usr/bin/env python3
'''
script that provides some stats about Nginx logs stored in MongoDB
'''
from pymongo import MongoClient


def log_stats():
    # Connect to MongoDB
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    collection = db.nginx

    # Count total logs
    total_logs = collection.count_documents({})

    # Count methods: GET, POST, PUT, PATCH, DELETE
    methods_count = {
        "GET": collection.count_documents({"method": "GET"}),
        "POST": collection.count_documents({"method": "POST"}),
        "PUT": collection.count_documents({"method": "PUT"}),
        "PATCH": collection.count_documents({"method": "PATCH"}),
        "DELETE": collection.count_documents({"method": "DELETE"})
    }

    # Count status check: method=GET, path=/status
    status_check_count = collection.count_documents({"method": "GET",
                                                    "path": "/status"})

    # Print results
    print(f"{total_logs} logs")
    print("Methods:")
    for method, count in methods_count.items():
        print(f"\tmethod {method}: {count}")
    print(f"{status_check_count} status check")


if __name__ == "__main__":
    log_stats()
