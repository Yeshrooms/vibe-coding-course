
# ## Hello World Gemini! 🤖
# 
# Now let's connect to Google's Gemini AI using the developer API! First, we need to install the required library and set up our API key.
# 
# [Instructions](https://ai.google.dev/gemini-api/docs/quickstart?lang=python)

# Install the Google Generative AI library
# Run this once: pip install google-genai

import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client()

response = client.models.generate_content(
    model="gemini-3.5-flash", contents="Tell me a good joke about vibe coders!"
)
print(response.text)



import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ['GEMINI_API_KEY'],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# response = client.chat.completions.create(
#     model="gemini-3.5-flash",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {
#             "role": "user",
#             "content": "Explain to me how vibe coding is in a few words"
#         }
#     ]
# )

# if response.choices[0]:
#     print(response.choices[0].message.content)

# Let's create a more interactive example
def chat_with_gemini(max_user_turns:int = 5):
    messages=[
            {"role": "system", "content": "You are a helpful assistant. Today's date is Friday July 17th. "
            "all of your answers should be concise and short, like a conversation, but should not be missing any information"
            "additionally, the current finalists of the world cup this year are spain (who beat france) and argentina (who beat england) "
            "you should not be talking about any of these things unless asked about it though"},
        ]
    count=0
    client = OpenAI(
        api_key=os.environ['GEMINI_API_KEY'],
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    
    print("Let's chat with Gemini!")
    while count < 5:
        request = input('User: ')
        if request.strip() == 'q':
            print('Exiting!')
            break
        while True:
            if request:
                messages.append({'role': 'user', 'content': request})
                break
            else:
                print('Please provide a valid message (cannot be empty)')
        response = client.chat.completions.create(
            model="gemini-3.5-flash",
            messages=messages
        )
        count+=1
        if response.choices[0]:
            messages.append(
                {"role": "assistant", "content": response.choices[0].message.content}
            )
            print(f'Assistant: {response.choices[0].message.content}')
    print('Reached Chat Limit!')
    
# Run our interactive chat
chat_with_gemini()


# ## Next Steps
# 
# Congratulations! You've learned:
# - Python basics (variables, data types)
# - Lists and how to work with them
# - For loops and while loops
# - How to connect to Google's Gemini AI API
# 
# Try experimenting with different prompts to Gemini, or combine what you've learned to create more complex programs!
