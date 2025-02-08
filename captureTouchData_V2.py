#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import time
import logging
import threading
from TP_lib import icnt86
from TP_lib import epd2in9_V2

logging.basicConfig(level=logging.DEBUG)
flag_t = 1


def pthread_irq():
    print("pthread irq running")
    while flag_t == 1:
        if (tp.digital_read(tp.INT) == 0):
            ICNT_Dev.Touch = 1
        else:
            ICNT_Dev.Touch = 0
        time.sleep(0.01)
    print("thread irq: exit")


try:
    logging.info("epd2in9_V2 Touch Demo")

    epd = epd2in9_V2.EPD_2IN9_V2()
    tp = icnt86.INCT86()
    ICNT_Dev = icnt86.ICNT_Development()
    ICNT_Old = icnt86.ICNT_Development()

    # Initialize display and touch
    epd.init()
    tp.ICNT_Init()
    epd.Clear(0xFF)

    t1 = threading.Thread(target=pthread_irq)
    t1.setDaemon(True)
    t1.start()

    while (1):
        tp.ICNT_Scan(ICNT_Dev, ICNT_Old)

        if (ICNT_Old.X[0] == ICNT_Dev.X[0] and ICNT_Old.Y[0] == ICNT_Dev.Y[0]):
            continue

        if (ICNT_Dev.TouchCount):
            ICNT_Dev.TouchCount = 0
            # Print the touch coordinates
            print(f"Touch detected at X: {ICNT_Dev.X[0]}, Y: {ICNT_Dev.Y[0]}")

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