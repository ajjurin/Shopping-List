#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import time
import logging
from PIL import Image, ImageDraw
import threading

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic/2in9')
fontdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from TP_lib import icnt86
from TP_lib import epd2in9_V2

logging.basicConfig(level=logging.DEBUG)
flag_t = 1

# Display resolution (296x128 for the 2.9-inch Waveshare e-paper display)
SCREEN_WIDTH = 296
SCREEN_HEIGHT = 128

# Touch screen resolution (you may need to adjust this based on your device's resolution)
TOUCH_WIDTH = 1024
TOUCH_HEIGHT = 600


def pthread_irq():
    print("pthread irq running")
    while flag_t == 1:
        if (tp.digital_read(tp.INT) == 0):
            ICNT_Dev.Touch = 1
        else:
            ICNT_Dev.Touch = 0
        time.sleep(0.01)
    print("thread irq: exit")


def draw_point_on_screen(draw, x, y):
    draw.line([x - 2, y, x + 2, y], fill=0)  # Horizontal line
    draw.line([x, y - 2, x, y + 2], fill=0)  # Vertical line


def reset_screen():
    image = Image.new('1', (epd.width, epd.height), 255)  # White background
    draw = ImageDraw.Draw(image)
    epd.display_Base(epd.getbuffer(image))  # Update the display with the cleared screen


def print_touch_coordinates(x, y):
    print(f"Touch detected at: x={x}, y={y}")


def map_coordinates(raw_x, raw_y):
    # Swap X and Y coordinates
    x = int(raw_y * SCREEN_WIDTH / TOUCH_HEIGHT)
    y = int(raw_x * SCREEN_HEIGHT / TOUCH_WIDTH)
    print(f"Raw touch: x={raw_x}, y={raw_y} => Swapped coordinates: x={x}, y={y}")
    x = max(0, min(x, SCREEN_WIDTH - 1))
    y = max(0, min(y, SCREEN_HEIGHT - 1))
    print(f"Clamped coordinates: x={x}, y={y}")
    return x, y


try:
    logging.info("epd2in9_V2 Touch Demo")

    epd = epd2in9_V2.EPD_2IN9_V2()
    tp = icnt86.INCT86()
    ICNT_Dev = icnt86.ICNT_Development()
    ICNT_Old = icnt86.ICNT_Development()

    logging.info("init and Clear")
    epd.init()
    tp.ICNT_Init()
    epd.Clear(0xFF)

    t1 = threading.Thread(target=pthread_irq)
    t1.setDaemon(True)
    t1.start()

    image = Image.new('1', (epd.width, epd.height), 255)  # White background
    draw = ImageDraw.Draw(image)
    epd.display_Base(epd.getbuffer(image))

    # Dummy input test
    for i in range(0, 128, 4):  # Moving down in a vertical axis with increments of 4
        raw_x = TOUCH_WIDTH // 4  # Fixed at 1/4 of the width
        raw_y = i * (TOUCH_HEIGHT // SCREEN_HEIGHT)  # Scale Y input
        mapped_x, mapped_y = map_coordinates(raw_x, raw_y)
        draw_point_on_screen(draw, mapped_x, mapped_y)
        epd.display_Partial_Wait(epd.getbuffer(image))
        time.sleep(0.5)

    while True:
        tp.ICNT_Scan(ICNT_Dev, ICNT_Old)
        if ICNT_Dev.TouchCount:
            ICNT_Dev.TouchCount = 0
            raw_x = ICNT_Dev.X[0]  # Assuming the first touch point
            raw_y = ICNT_Dev.Y[0]  # Assuming the first touch point
            print(f"Touch detected at: x={raw_x}, y={raw_y}")
            mapped_x, mapped_y = map_coordinates(raw_x, raw_y)
            draw_point_on_screen(draw, mapped_x, mapped_y)
            epd.display_Partial_Wait(epd.getbuffer(image))
        time.sleep(0.01)

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    flag_t = 0
    epd.sleep()
    time.sleep(2)
    t1.join()
    epd.Dev_exit()
    exit()
