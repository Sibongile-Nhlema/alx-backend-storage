#!/usr/bin/env python3
'''
Module handles function that returns all students sorted by average score
'''


def top_students(mongo_collection):
    '''
    function that returns all students sorted by average score
    Args:
        mongo_collection (obj): pymongo collection object
    Returns:
        list: ordered list of students and their averages
    '''
    pipeline = [
        {
            "$addFields": {
                "averageScore": { "$avg": "$topics.score" }
            }
        },
        {
            "$sort": { "averageScore": -1 }
        }
    ]
    return list(mongo_collection.aggregate(pipeline))
