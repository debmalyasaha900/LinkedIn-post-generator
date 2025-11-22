import pandas as pd
from db import posts_col   # import posts collection from db.py

class FewShotPosts:
    def __init__(self):
        self.df = None
        self.unique_tags = None
        self.load_posts()

    def clean_tag(self, tag):
        if not isinstance(tag, str):
            return ""

        # Normalize variations of same concept
        tag = tag.replace("-", " ")  # e.g. self-reflection → self reflection
        tag = tag.replace("_", " ")  # e.g. self_reflection → self reflection

        # Fix common duplicates
        replacements = {
            "self reflection": "Self-Reflection",
            "selfreflection": "Self-Reflection",
            "selfrespect": "Self-Respect",
            "sucess": "Success",
            "succcess": "Success",
            "psycology": "Psychology",
            "placement": "Placement",
            "placements": "Placement",
            "internships": "Internship",
        }

        tag_lower = tag.lower().strip()

        if tag_lower in replacements:
            return replacements[tag_lower]

        return tag.title()

    def load_posts(self):
        posts = list(posts_col.find({}, {"_id": 0}))

        if len(posts) == 0:
            print("⚠ No posts found in MongoDB!")
            self.df = pd.DataFrame()
            self.unique_tags = set()
            return

        df = pd.json_normalize(posts)

        # Fix missing fields
        if "line_count" not in df:
            df["line_count"] = df["text"].apply(lambda x: len(str(x).split("\n")))

        if "tags" not in df:
            df["tags"] = df["text"].apply(lambda x: ["General"])

        df["length"] = df["line_count"].apply(self.categorize_length)

        # Collect tags safely
        df["tags"] = df["tags"].apply(lambda t: t if isinstance(t, list) else [])
        all_tags = (
            df["tags"]
            .explode()
            .dropna()
            .apply(self.clean_tag)
            .unique()
        )

        self.df = df
        self.unique_tags = set(all_tags)

    def categorize_length(self, line_count):
        if line_count < 5:
            return "Short"
        elif 5 <= line_count <= 10:
            return "Medium"
        else:
            return "Long"

    def get_tags(self):
        return sorted(list(self.unique_tags))

    def get_tags_for_influencer(self, influencer):
        influencer_df = self.df[self.df["influencer"] == influencer]

        tags_series = influencer_df["tags"]

        # CLEAN TAGS here also
        flat_tags = (
            tags_series
            .explode()
            .dropna()
            .apply(self.clean_tag)
            .unique()
        )

        return sorted(flat_tags)

    def get_filtered_post(self, influencer, language, length, tag):
        df = self.df.copy()

        # Level 1 — strict filter
        df_f = df[
            (df["influencer"] == influencer) &
            (df["language"].str.lower() == language.lower()) &
            (df["length"].str.lower() == length.lower()) &
            (df["tags"].apply(lambda t: tag.lower() in [x.lower() for x in t]))
            ]
        if len(df_f) > 0:
            return df_f.to_dict(orient="records")

        # Level 2 — remove length filter
        df_f = df[
            (df["influencer"] == influencer) &
            (df["language"].str.lower() == language.lower()) &
            (df["tags"].apply(lambda t: tag.lower() in [x.lower() for x in t]))
            ]
        if len(df_f) > 0:
            return df_f.to_dict(orient="records")

        # Level 3 — remove tag filter
        df_f = df[
            (df["influencer"] == influencer) &
            (df["language"].str.lower() == language.lower())
            ]
        if len(df_f) > 0:
            return df_f.to_dict(orient="records")

        # Level 4 — return top 2 posts from influencer
        fallback = df[df["influencer"] == influencer].head(2)
        return fallback.to_dict(orient="records")



