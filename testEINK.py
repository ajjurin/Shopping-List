from waveshare_epd import epd2in9_V2
from PIL import Image, ImageDraw, ImageFont

epd = epd2in9_V2.EPD_2IN9_V2()
epd.init()
epd.Clear()

# Create an image with correct dimensions
image = Image.new('1', (296, 128), 255)  # Landscape orientation
draw = ImageDraw.Draw(image)

# Draw something on the image
font = ImageFont.load_default()
draw.text((10, 10), "Hello, e-Ink!", font=font, fill=0)  # Black text

# Save the image to check it visually
image.save("test_output.bmp")
print("Image saved to test_output.bmp")

# Send the buffer to the display
epd.display(epd.getbuffer(image))
epd.sleep()
