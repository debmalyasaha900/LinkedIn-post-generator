from llm_helper import llm
from few_shots import FewShotPosts

few_shot = FewShotPosts()

# Convert UI length to a readable value
def get_length_str(length):
    if length == "Short":
        return "1 to 5 lines"
    if length == "Medium":
        return "6 to 10 lines"
    if length == "Long":
        return "11 to 15 lines"


def generate_post(influencer, length, language, tag):
    """
    influencer → comes from dropdown in Streamlit
    """
    prompt = get_prompt(influencer, length, language, tag)
    response = llm.invoke(prompt)
    raw = response.content.strip()

    # remove surrounding quotes if any
    if (raw.startswith('"') and raw.endswith('"')) or (raw.startswith("'") and raw.endswith("'")):
        raw = raw[1:-1].strip()

    return raw


def get_prompt(influencer, length, language, tag):
    length_str = get_length_str(length)

    # Base prompt
    prompt = f"""
Generate a LinkedIn post using the below information. No preamble.

1) Influencer: {influencer}
2) Topic: {tag}
3) Length: {length_str}
4) Language: {language}
If Language is Hinglish then it means it is a mix of Hindi and English.(Hindi+English)
The script for the generated post should always be English.
Strictly NO PREAMBLE.
Just generate a text to post don't add quotation marks before and after the text
"""

    # Fetch few-shot examples
    examples = few_shot.get_filtered_post(
        influencer=influencer,
        language=language,
        length=length,
        tag=tag
    )

    # Add examples if available
    if len(examples) > 0:
        prompt += "\n5) Use the writing style as per the following examples:"

    for i, post in enumerate(examples):
        prompt += f"\n\nExample {i+1}:\n{post['text']}\n"
        if i == 9:   # Only 2 examples max
            break

    return prompt


# Debug test
if __name__ == "__main__":
    print(generate_post("Ankur Warikoo", "Medium", "English", "Mental Health"))
