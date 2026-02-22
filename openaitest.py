from openai import OpenAI          # 
from config import apikey

print(f"API Key loaded: {apikey[:8]}...")

client = OpenAI(api_key=apikey)    

response = client.chat.completions.create(  
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

print(response.choices[0].message.content)
