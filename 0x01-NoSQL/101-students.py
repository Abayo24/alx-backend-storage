#!/usr/bin/env python3
"""function that returns all students sorted by average score"""


from pymongo import DESCENDING


def top_students(mongo_collection):
    """returns all students sorted by average score"""
    pipeline = [{
        "$project": {
            "name": 1,
            "averageScore": {
                "$avg": "$topics.score"
                }
            }
        },
        {"$sort": {
            "averageScore": DESCENDING
            }
        }
     ]

    result = mongo_collection.aggregate(pipeline)
    return result
