from openai import OpenAI
from config import config

## generate response from openai 
async def generate_openai_response(message):
    try:
        client = OpenAI(api_key= config.get("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role":"user", "content": f"{message}"}]
        )

        return response.choices[0].message.content.strip()
    except Exception as e:
        print(e)

## remove new lines from openai response
def remove_newlines(text):
    return text.replace("\n", "")