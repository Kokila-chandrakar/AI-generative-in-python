from openai import OpenAI

#pip install openai
#if you saved the key under a diffrent enviroment variable name, you can do something like:
client = OpenAI(
api_key= os.getenv("OPENAI_API_KEY")


completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named alexa skilled in general tasks like google cloud."},
        {"role": "user", "content": "what is coding."}
    ]
)

print(completion.choices[0].message.content)