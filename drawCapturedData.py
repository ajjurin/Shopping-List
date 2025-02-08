import sys
from waveshare_epd import epd2in9_V2
from PIL import Image, ImageDraw
from evdev import InputDevice, categorize, ecodes

# Initialize the e-paper display
epd = epd2in9_V2.EPD_2IN9_V2()
epd.init()
epd.Clear(255)

# Create an image object for drawing
image = Image.new('1', (296, 128), 255)  # Adjust to e-ink resolution
draw = ImageDraw.Draw(image)

# Initialize touch input device
device = InputDevice('/dev/input/event0')  # Change to match your device

# Replace with actual max values from `captureTouchData`
touchscreen_max_x = 4096
touchscreen_max_y = 4096

# Map touchscreen coordinates to e-ink resolution
def map_coordinates(x, y):
    mapped_x = int(x * 296 / touchscreen_max_x)
    mapped_y = int(y * 128 / touchscreen_max_y)
    return mapped_x, mapped_y

# List to store touch points
points = []

try:
    print("Touchscreen ready. Draw on the screen...")
    for event in device.read_loop():
        if event.type == ecodes.EV_ABS:
            absevent = categorize(event)
            if absevent.event.code == ecodes.ABS_X:
                x = absevent.event.value
            elif absevent.event.code == ecodes.ABS_Y:
                y = absevent.event.value
                mapped_x, mapped_y = map_coordinates(x, y)
                points.append((mapped_x, mapped_y))

                # Draw the line between the last two points
                if len(points) > 1:
                    draw.line([points[-2], points[-1]], fill=0, width=2)

                # Update the e-ink display periodically
                epd.display(epd.getbuffer(image))

except KeyboardInterrupt:
    print("Exiting...")
    epd.sleep()
    sys.exit()
