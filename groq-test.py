from groq import Groq
import os
import requests

from dotenv import load_dotenv, dotenv_values 
# loading variables from .env file
load_dotenv() 

api_key = os.getenv("GROQ_API_KEY")

client = Groq(
    api_key=api_key,
)

# chat_completion = client.chat.completions.create(
#     messages=[
#         {
#             "role": "user",
#             "content": "Explain the importance of fast language models",
#         }
#     ],
#     model="llama3-8b-8192",
#     stream=False,
# )

# print(chat_completion.choices[0].message.content)

url = "https://api.groq.com/openai/v1/models"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)

print(response.json())