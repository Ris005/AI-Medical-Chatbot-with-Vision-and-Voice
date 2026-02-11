import os
import base64
from groq import Groq

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")  # Make sure this is set in your environment

# -------------------------------
# ENCODE IMAGE
# -------------------------------
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# -------------------------------
# ANALYZE IMAGE WITH QUERY
# -------------------------------
def analyze_image_with_query(query, encoded_image, model):
    client = Groq(api_key=GROQ_API_KEY)  # initialize Groq client

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": query},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}
                },
            ],
        }
    ]

    chat_completion = client.chat.completions.create(
        messages=messages,
        model=model
    )

    # Return the text response
    return chat_completion.choices[0].message.content

#http://127.0.0.1:7860