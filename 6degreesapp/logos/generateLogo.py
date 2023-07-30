import openai
import requests
from PIL import Image
from io import BytesIO
import os
openai.api_key = os.getenv("OPENAI_API_KEY")

for i in range(5):  # Number of iterations you want
    response = openai.Image.create_variation(
        image=open("logo3.png","rb"),
        size="512x512",
    )
    url = response['data'][0]['url']
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img.save(f"image{i}.png")  # Save image to your directory

words = "generate a cartoonish snowflake that is well formed, smooth, symmetrical and vibrant. it should have 6 protrusions and a circular center"




"""
for i in range(5):  # Number of iterations you want
    response = openai.Image.create(
        prompt=words,
        n=1,
        size="512x512",
    )
    url = response['data'][0]['url']
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img.save(f"image{i}.png")
"""