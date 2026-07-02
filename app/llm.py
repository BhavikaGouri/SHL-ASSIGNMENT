import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GENAI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")
def generate_reply(query, retrieved_docs):

    context = ""

    for doc in retrieved_docs:
        context += f"""
Title: {doc['title']}
URL: {doc['url']}

Content:
{doc['content']}

---------------------
"""

    prompt = f"""
You are an SHL Assessment Recommendation Assistant.

Only answer using the SHL documents below.
Compare the user's query with the content of the documents.
If information is missing,
say you don't know.

Never invent assessments.

Context:

{context}

User:

{query}

Respond naturally.
"""

    response = model.generate_content(prompt)

    return response.text