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
    # Check if the document exists
    existing_school = mongo_collection.find_one({"name": name})
    if existing_school:
        # Update topics for the found document
        mongo_collection.update_one(
            {"name": name},
            {"$set": {"topics": topics}}
        )
    else:
        # Handle case where document with 'name' does not exist
        print(f"Document with name '{name}' not found. Skipping update.")
