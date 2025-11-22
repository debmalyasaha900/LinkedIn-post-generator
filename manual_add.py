from db import insert_post
from processed_posts import extract_metadata

text = """Let’s be careful:
If Indo-Pak tensions escalate, brace for economic tremors:
- Rupee may wobble
- Foreign investors flee to safer shores
-Oil prices could spike
- Defence spending shoots up, infra takes a backseat
- Markets dive.
War weakens economies. Even for the winner.
"""
likes = 801
comments = 134
influencer = "Harsh Goenka"

meta = extract_metadata(text)

post = {
    "influencer": influencer,
    "text": text,
    "likes": likes,
    "comments": comments,
    "line_count": meta["line_count"],
    "language": meta["language"],
    "tags": meta["tags"]
}

insert_post(post)
print("Saved!")
