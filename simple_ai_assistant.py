from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv() #by default looks for .env file

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

messages = []

messages.append(
          {
                "role":"system",
                "content":"act as a humble ai assistant and answer in less than 50 words"
          }
    )


while True:
    user_input = input("\nYOU: ")

    if user_input.lower() in ["exit" , "quit", "end", "bye", "see ya"]:
            break

    messages.append(
          {
                "role":"user",
                "content":user_input
          }
    )
    
    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=messages
    )

    messages.append(
              {
                    "role":"assistant",
                    "content":response.choices[0].message.content
              }
        )

    print("Assistant: " + response.choices[0].message.content)

