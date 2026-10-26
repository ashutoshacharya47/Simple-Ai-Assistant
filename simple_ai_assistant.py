from openai import OpenAI
from dotenv import load_dotenv
from tools import TOOLS , FUNCTION_NAME_TO_FUNCTION_MAP
import json
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
            messages=messages,
            tools = TOOLS
      )

      msg = response.choices[0].message

      if msg.tool_calls:
            messages.append(msg)

            for tool_call in msg.tool_calls:
                  func_name = tool_call.function.name
                  func_args = json.loads(tool_call.function.arguments or  {})

                  fn = FUNCTION_NAME_TO_FUNCTION_MAP[func_name]
                  result = fn(**func_args)

                  messages.append({
                        "role" : "tool",
                        "tool_id" : "tool_call.id",
                        "content": str(result)
                  })

            response = client.chat.completions.create(
                    model=os.getenv("MODEL"),
                    messages=messages
                )
            
            msg = response.choices[0].message


      messages.append({
            "role" : "assistane",
            "content" : msg.content
      })

      print("Assistant: " + msg.content)

