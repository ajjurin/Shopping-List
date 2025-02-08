#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import time
import logging
from PIL import Image, ImageDraw, ImageFont
import threading

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic/2in9')
fontdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from TP_lib import icnt86
from TP_lib import epd2in9_V2

logging.basicConfig(level=logging.DEBUG)
flag_t = 1

# Global variables to store previous touch coordinates
last_x, last_y = None, None


def pthread_irq():
    print("pthread irq running")
    while flag_t == 1:
        if (tp.digital_read(tp.INT) == 0):
            ICNT_Dev.Touch = 1
        else:
            ICNT_Dev.Touch = 0
        time.sleep(0.01)
    print("thread irq: exit")


def draw_on_screen(draw, x, y):
    global last_x, last_y

    # If there is a previous touch, draw a line from last touch to the new touch
    if last_x is not None and last_y is not None:
        draw.line([last_x, last_y, x, y], fill=0, width=2)  # Drawing black line with width 2
    last_x, last_y = x, y


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

    # Create a blank white image to draw on
    image = Image.new('1', (epd.width, epd.height), 255)  # White background
    draw = ImageDraw.Draw(image)

    epd.display_Base(epd.getbuffer(image))

    while True:
        tp.ICNT_Scan(ICNT_Dev, ICNT_Old)
        if ICNT_Dev.TouchCount:
            ICNT_Dev.TouchCount = 0

            # Get touch coordinates
            x = ICNT_Dev.X[0]
            y = ICNT_Dev.Y[0]
            print(f"Touch detected at: x={x}, y={y}")

            # Draw on the screen
            draw_on_screen(draw, x, y)

            # Update the display with the drawn image
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
