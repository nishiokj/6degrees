import cv2
import numpy as np
from PIL import Image
"""
# Read image using OpenCV
img = cv2.imread('logo1.png', -1)

# Convert the image to gray scale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Find the edges in the image using the Canny edge detection method
edges = cv2.Canny(gray, 50, 150)

# Dilate the edges to make them more pronounced
dilated = cv2.dilate(edges, None)

# Convert the dilated image to a PIL Image and get the alpha band of the original image
edges_pil = Image.fromarray(dilated)
alpha = Image.fromarray(img[:, :, 3])

# Paste the edges onto the alpha band using the edges as a mask
alpha.paste(edges_pil, mask=edges_pil)

# Put the new alpha band back into the original image
img[:, :, 3] = np.array(alpha)

# Save the result
cv2.imwrite('logo_with_border.png', img)

"""
# Read image using OpenCV
img = cv2.imread('logo9.png', -1)

# Convert the image to gray scale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Find the edges in the image using the Canny edge detection method
edges = cv2.Canny(gray, 50, 150)

# Create a larger structuring element for more dilation (thickness of border)
kernel = np.ones((5,5),np.uint8)

# Dilate the edges to make them more pronounced
dilated = cv2.dilate(edges, kernel, iterations = 2)

# Prepare the mask with 3 channels, initially set to 0
mask = np.zeros_like(img, dtype=np.uint8)

# Set the border color to white
color = [0, 0, 0]

# Set the pixels where the dilated image is white to the border color
for i in range(3):
    mask[:,:,i] = dilated

# Create the border by adding the mask to the image
bordered_img = cv2.addWeighted(img, 1, mask, 1, 0)

# Save the result
cv2.imwrite('logo_with_white_border.png', bordered_img)
