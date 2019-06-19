import time
import board
import digitalio
import samd21_get_temperature
import light_follows_button

def main():
    while True:
        try:
            switch = digitalio.DigitalInOut(board.D7)
            switch.direction = digitalio.Direction.INPUT
            switch.pull = digitalio.Pull.UP
            while True:
                #print(str(switch.value))
                if switch.value: # slide switch = left
                    print("slide switch = left")
                    samd21_get_temperature.main()
                else: # slide switch = right
                    print("slide switch = right")
                    print("halting")
                    #light_follows_button.main()
                    return 0 # allow access to REPL via "miniterm.py /dev/ttyACM0"
                time.sleep(1)
        except:
            print("got unhandled exception in code.py")
            try:
                switch.deinit()
            except:
                pass
            #import time
            #import board
            #import digitalio
            #led = digitalio.DigitalInOut(board.D13)
            #led.direction = digitalio.Direction.OUTPUT
            #led.value = True
            #time.sleep(1)
            #led.value = False
            #time.sleep(1)
            #led.value = True
            #time.sleep(1)
            #led.value = False
            #time.sleep(1)
            #import erase
            #erase.main()
        time.sleep(1)

if __name__ == '__main__':
    main()

