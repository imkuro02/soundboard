import os
import serial
import threading
import serial
from time import sleep
import player


def main():
    p = player.player()
    serialPort = serial.Serial(
        port="/dev/ttyUSB0", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE
    )

    serialString = ""  # Used to hold data coming over UART

    while 1:
        sleep(.05)
        # Wait until there is data waiting in the serial buffer
        if serialPort.in_waiting > 0:
            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline()
            # Print the contents of the serial data
            try:
                output = serialString.decode("Ascii")
                if len(output) != 0:
                    print(output)
                    if '1' in output : p.play_sound('bruh.wav') 
                    if '2' in output : p.play_sound('fart.wav') 

            except Exception as e:
                print(e)


if __name__ == '__main__':


    # ./create_sink.sh

    main()

    # pulsaudio -k
    #play_sound()

