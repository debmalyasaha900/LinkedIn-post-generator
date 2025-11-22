import os
import streamlit as st
from pymongo import MongoClient


if "MONGO_URI" in st.secrets:   # Streamlit Cloud
    MONGO_URI = st.secrets["MONGO_URI"]

elif "MONGO_URI" in os.environ:  # Local .env
    MONGO_URI = os.environ["MONGO_URI"]

else:
    raise ValueError("❌ MONGO_URI not found in Streamlit Secrets or .env file!")


client = MongoClient(MONGO_URI)
db = client["LinkedIn_posts_db"]

# Collections
influencers_col = db["influencers"]
posts_col = db["posts"]


def get_all_influencers():
    return list(influencers_col.find({}, {"_id": 0}))

def insert_influencer(data: dict):
    return influencers_col.insert_one(data)

def insert_post(data: dict):
    return posts_col.insert_one(data)

def get_filtered_posts(influencer=None, language=None, length=None, tag=None):
    query = {}

    if influencer:
        query["influencer"] = influencer
    if language:
        query["language"] = language
    if length:
        query["length"] = length
    if tag:
        query["tags"] = tag

    return list(posts_col.find(query, {"_id": 0}))
