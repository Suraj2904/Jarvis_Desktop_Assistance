# openaitest.py — fixed for openai >= 1.0.0

from openai import OpenAI          # FIX 1: v1.0+ uses client, not openai.ChatCompletion
from config import apikey

print(f"API Key loaded: {apikey[:8]}...")

client = OpenAI(api_key=apikey)    # FIX 2: create a client instance

response = client.chat.completions.create(   # FIX 3: new method path
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Write an email to my boss for resignation."}
    ],
    temperature=1,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)

# FIX 4: v1.0+ response is an object, use dot notation not dict keys
print(response.choices[0].message.content)