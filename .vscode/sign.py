from PIL import Image, ImageDraw, ImageFont

# Create a blank image with a white background
width, height = 400, 100
image = Image.new('RGB', (width, height), 'white')
draw = ImageDraw.Draw(image)

# Load a font and set the font size
font = ImageFont.load_default()
font_size = 20

# Define the text for your signature
signature_text = "poornima"

# Calculate the width and height of the text
text_width, text_height = draw.textsize(signature_text, font)

# Calculate the position to center the text on the image
x = (width - text_width) / 2
y = (height - text_height) / 2

# Set the text color
text_color = (0, 0, 0) # Black

# Add the text to the image
draw.text((x, y), signature_text, fill=text_color, font=font)

# Save the signature as an image
image.save("signature.png")

# Display the signature
image.show()