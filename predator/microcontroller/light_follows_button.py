import board
import time
import digitalio

def main():
    try:
        led = digitalio.DigitalInOut(board.D13)
        led.direction = digitalio.Direction.OUTPUT
        button = digitalio.DigitalInOut(board.D5)
        button.direction = digitalio.Direction.INPUT
        button.pull = digitalio.Pull.DOWN
        soft_boot = digitalio.DigitalInOut(board.D4)
        soft_boot.direction = digitalio.Direction.INPUT
        soft_boot.pull = digitalio.Pull.DOWN
        xor = 0
        while True:
            led.value = xor ^ button.value
            if soft_boot.value:
                #xor = not xor
                #pass
                time.sleep(0.1)
                try:
                    led.deinit()
                except:
                    pass
                try:
                    button.deinit()
                except:
                    pass
                try:
                    soft_boot.deinit()
                except:
                    pass
                return 0
            time.sleep(0.01)
    except:
        print("got unhandled exception in light_follows_button.py")
        try:
            led.deinit()
        except:
            pass
        try:
            button.deinit()
        except:
            pass
        try:
            soft_boot.deinit()
        except:
            pass
        time.sleep(1)
        return 1

if __name__ == '__main__':
    main()

