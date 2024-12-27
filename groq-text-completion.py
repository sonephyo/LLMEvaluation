from groq import Groq
import os

from dotenv import load_dotenv, dotenv_values

# loading variables from .env file
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

client = Groq(
    api_key=api_key,
)

chat_completion = client.chat.completions.create(
    #
    # Required parameters
    #
    messages=[
        {"role": "system", "content": "you are a pirate."},
        {
            "role": "user",
            "content": "Explain the importance of fast language models",
        },
    ],
    model="llama3-8b-8192",
    temperature=0.5,
    max_tokens=1024,
    top_p=1,
    stop=None,
    stream=False,
)

# Print the completion returned by the LLM.
print(chat_completion.choices[0].message.content)


print("-----")
completion = client.chat.completions.create(
    model="llama3-70b-8192",
    messages=[
        {
            "role": "user",
            "content": "Write a Python function to calculate the factorial of a number.",
        },
        {"role": "assistant", "content": "```python"},
    ],
    stop="```",
)

print(completion.choices[0].message.content)