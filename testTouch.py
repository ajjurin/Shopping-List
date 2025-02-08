import time
from TP_lib import icnt86

tp = icnt86.INCT86()
ICNT_Dev = icnt86.ICNT_Development()
ICNT_Old = icnt86.ICNT_Development()

tp.ICNT_Init()  # Initialize the touchscreen
print("Touchscreen initialized.")

while True:
    tp.ICNT_Scan(ICNT_Dev, ICNT_Old)
    if ICNT_Dev.TouchCount > 0:
        ICNT_Dev.TouchCount = 0
        x, y = ICNT_Dev.X[0], ICNT_Dev.Y[0]
        print(f"Touch detected at X: {x}, Y: {y}")
    time.sleep(0.1)  # Small delay to prevent CPU overload
