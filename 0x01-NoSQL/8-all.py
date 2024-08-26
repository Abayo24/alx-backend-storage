#!/usr/bin/env python3
"""
function that lists all documents in a collection
"""


def list_all(mongo_collection):
    """lists all documents in a collection"""
    if mongo_collection.length == 0:
        return []
    return mongo_collection.find()
