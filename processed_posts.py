import json
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from llm_helper import llm

# 👉 import your db collections
from db import posts_col

def process_post(raw_file_path):
    enriched_posts = []

    # 1) Load raw posts
    with open(raw_file_path, "r", encoding="utf-8") as file:
        posts = json.load(file)

    # 2) Extract metadata for each post
    for post in posts:
        metadata = extract_metadata(post["text"])
        processed = post | metadata      # merge dicts
        enriched_posts.append(processed)

    # 3) Unify tags for all posts
    unified_tags = get_unified_tags(enriched_posts)

    # 4) Rewrite unified tags
    for post in enriched_posts:
        post["tags"] = list({unified_tags[tag] for tag in post["tags"]})

    # 5) INSERT INTO MONGO
    posts_col.insert_many(enriched_posts)

    print("✅ Upload complete: All posts inserted into MongoDB.")


def get_unified_tags(processed_posts):
    unique_tags = set()
    for post in processed_posts:
        unique_tags.update(post["tags"])

    unique_tags_list = ", ".join(unique_tags)

    template = """
    I will give you a list of tags. Unify them as per rules:
    1) Merge similar tags (Jobseekers → Job Search, Inspiration → Motivation)
    2) Title Case
    3) Return JSON ONLY (no preamble)

    Tags:
    {tags}
    """

    prompt = PromptTemplate.from_template(template)
    chain = prompt | llm
    response = chain.invoke({"tags": unique_tags_list})

    try:
        parser = JsonOutputParser()
        return parser.parse(response.content)
    except Exception:
        raise OutputParserException("Could not parse unified tag JSON.")


def extract_metadata(post_text):
    template = """
    Extract metadata from this LinkedIn post:
    1) Return JSON only
    2) Keys: line_count, language, tags
    3) Max 2 tags
    4) Language = English or Hinglish

    Post:
    {post}
    """

    prompt = PromptTemplate.from_template(template)
    chain = prompt | llm
    response = chain.invoke({"post": post_text})

    try:
        parser = JsonOutputParser()
        return parser.parse(response.content)
    except Exception:
        raise OutputParserException("Cannot parse metadata JSON.")


if __name__ == "__main__":
    process_post("data/raw_posts.json")
