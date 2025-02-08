from evdev import InputDevice, categorize, ecodes
import time

# Replace 'event0' with the correct input event for your touchscreen.
# Use `ls /dev/input/` to find the event number of your device (usually something like 'event0', 'event1', etc.)
device = InputDevice('/dev/input/event0')

# Print device info
print(device)

# Loop to capture the events
for event in device.read_loop():
    if event.type == ecodes.EV_ABS:
        absevent = categorize(event)
        if absevent.event.code == ecodes.ABS_X:
            x = absevent.event.value
        elif absevent.event.code == ecodes.ABS_Y:
            y = absevent.event.value
            # Print the x and y values, you can store them for drawing later
            print(f"Touch at ({x}, {y})")
