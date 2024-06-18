#!/usr/bin/env python3
'''
Module for a python function that udages the topics of a school document
'''


def update_topics(mongo_collection, name, topics):
    '''
    function that changes all topics of a school document based on the name
    Args:
        mongo_collection (obj): pymongo collection object
        name (str): school name to update
        topics (list of str): list of topics approached in the school
    '''
    mongo_collection.update_one({"name": name}, {"$set": {"topics": topics}})
