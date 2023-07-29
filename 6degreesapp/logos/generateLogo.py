import openai
import requests
from PIL import Image
from io import BytesIO
import os
openai.api_key = os.getenv("OPENAI_API_KEY")
"""
for i in range(5):  # Number of iterations you want
    response = openai.Image.create_variation(
        image=open("candidate8.png","rb"),
        size="512x512",
    )
    url = response['data'][0]['url']
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img.save(f"image{i}.png")  # Save image to your directory
"""
def add_border(input_image_path, output_image_path, border_color, border_size):
    image = Image.open(input_image_path)

    # Create a new image that is larger by border_size on all sides
    new_image = Image.new("RGBA", (image.width + 2 * border_size, image.height + 2 * border_size), border_color)

    # Paste the original image into the center of the new image
    new_image.paste(image, (border_size, border_size))

    # Save the new image
    new_image.save(output_image_path)

# Use the function

add_border("logo.png", "logo_with_border.png", (255, 255, 255, 255), 10)