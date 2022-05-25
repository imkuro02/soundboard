import os
import serial
import threading
import serial
import random
from time import sleep
import player
import volume
from pathlib import Path
import atexit
import signal

P = player.player()

def handle_exit():
    print('exiting')
    P.cleanup()

atexit.register(handle_exit)
signal.signal(signal.SIGTERM, handle_exit)
signal.signal(signal.SIGINT, handle_exit)


print('2022-05-25 235800')

def reload_player(p):
    for i in range(0,6):
        sleep(10)
        P.cleanup(False) # if you dont say False here, module-null-sink will get removed
        print('reload: ',i)
    print('fully reloaded')


def main():
    layer = 'a'
    P.init_modules()

    print('ready')

    # reloads a couple of times to make sure sox isnt slow
    # paused to check that if i wait before turning the software on after reboot it will 
    # act normal
    '''
    reloader = threading.Thread(target = reload_player, args=(p,))
    reloader.setDaemon(True)
    reloader.start()
    '''
    serialPort = serial.Serial(
        port="/dev/ttyUSB0", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE
    )

    serialString = ""  # Used to hold data coming over UART

    sleep(2) 

    while 1:
        serialPort.flush()
        sleep(.05)
        # Wait until there is data waiting in the serial buffer
        if serialPort.in_waiting > 0:
            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline()
            # Print the contents of the serial data
            output = serialString.decode("Ascii")

            # if it has tabs then its the volume sliders
            if '\t' in output:
                output = (f"{output}").split('\t')
                output = map(int, output)
                output = list(output)
                volume.change_volume(output)
            else:
                # last 4 buttons are volume slider links
                if int(output)>=6:
                    if '6' in output:
                        layer = 'a'
                    if '7' in output:
                        layer = 'b'
                    if '8' in output:
                        layer = 'c'
                    if '9' in output:
                        P.cleanup(False) # if you dont say False here, module-null-sink will get removed
                        volume.get_window()
                else: # if not the last 4 buttons then:
                    output = int(output)
                    path = f'sounds/{layer}{output}/'
                    sounds = os.listdir(path)
                    if len(sounds) > 0:
                        print(sounds)
                        sound = random.randrange(0, len(sounds))
                        P.play_sound(f'{path}{sounds[sound]}') 


            # this code gets current voice mode and sends that to arduino
            '''
            voice_mode = p.get_voice()
            print(voice_mode)
            serialPort.write(str(voice_mode).encode()+b'\n')
            '''

def setup():
    layers = 'a b c'.split()
    HOME = str(Path.home())
    PATH = f'{HOME}/.soundboard/' 
    if os.path.exists(PATH) == True:
        os.chdir(PATH)
        cwd = os.getcwd()
        return
    else:
        print('\nfirst time setup, creating ".soundboard"\n')
        os.makedirs(PATH) 
        os.makedirs(f'{PATH}/sounds/') 
        for i in range(0,5):
            for layer in layers:
                os.makedirs(f'{PATH}/sounds/{layer}{i}') 

        # this is dirty af, check volume.py 
        with open(f'{PATH}/settings.txt', 'w') as f:
            f.write('\n\n\n')
            f.close()

        os.chdir(PATH)


if __name__ == '__main__':
    setup()
    main()
