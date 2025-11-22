import json
from db import insert_post
from processed_posts import extract_metadata

# Path to your Apify JSON file
FILE_PATH = "data/scraped_posts.json"

with open(FILE_PATH, "r", encoding="utf-8") as f:
    scraped_data = json.load(f)

count = 0

for item in scraped_data:
    text = item.get("text", "")
    likes = item.get("likes", 0)
    comments = item.get("comments", 0)

    # generate metadata
    metadata = extract_metadata(text)

    post_data = {
        "influencer": "Ankur Warikoo",  # manually give influencer
        "text": text,
        "likes": likes,
        "comments": comments,
        "line_count": metadata["line_count"],
        "language": metadata["language"],
        "tags": metadata["tags"],
    }

    insert_post(post_data)
    count += 1

print(f"✅ Successfully imported {count} posts into MongoDB!")
