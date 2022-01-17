import os
import serial
import threading
import serial
import random
from time import sleep
import player


def main():
    try:
        p = player.player()

        for i in range(0,1):
            p.init_sound()
            sleep(5)
            p.cleanup()
        p.init_sound()
        print('ready')

        serialPort = serial.Serial(
            port="/dev/ttyUSB0", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE
        )

        serialString = ""  # Used to hold data coming over UART

        while 1:
            sleep(.1)
            # Wait until there is data waiting in the serial buffer
            if serialPort.in_waiting > 0:
                # Read data out of the buffer until a carraige return / new line is found
                serialString = serialPort.readline()
                # Print the contents of the serial data
                output = serialString.decode("Ascii")
                if len(output) != 0:
                    if '1' in output : p.play_sound('bruh.wav') 
                    index = random.randint(1, 11)
                    RAND = random.randint(-1000, 1000)
                    #if '2' in output : p.play_sound(f'moans/{index}.wav') 
                    if '2' in output : 
                        p.update_bind_default_mic() 

    finally:
        p.cleanup()


if __name__ == '__main__':


    # ./create_sink.sh

    main()

    # pulsaudio -k
    #play_sound()

