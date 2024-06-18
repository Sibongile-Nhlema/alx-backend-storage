#!/usr/bin/env python3
'''
Module handles the listing of all documents in a collection
'''


def list_all(mongo_collection):
    '''
    list all documents in a collection
    Args:
        mongo_collection: the given pymongo collection
    Returns:
        documents or empty list
    '''
    return list(mongo_collection.find()) if mongo_collection.count_documents({}) > 0 else []

