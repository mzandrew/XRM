import board
from digitalio import DigitalInOut, Direction, Pull

led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

switch = DigitalInOut(board.D5)
switch.direction = Direction.INPUT
switch.pull = Pull.UP   # Pull.Down is available on some MCUs

while True:
    led.value = not switch.value
    time.sleep(0.01)

