import os

from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
llm=ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"),model="meta-llama/llama-4-scout-17b-16e-instruct")

if __name__=="__main__":
    response=llm.invoke("What is the fullform of BGMI?")
    print(response.content)