from pillow import PIL
from PIL import Image

# Open an image file
image = Image.open('assets/mama_picture.jpg')

# Convert image to grayscale
bw_image = image.convert('L')

# Save the black and white image
bw_image.save('assets/convert_mama_picture_black_white.jpg')
