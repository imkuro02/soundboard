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


print('2022-12-15 221400')

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

    prev_output = [0,0,0,0]

    def myround(x, base=2):
        return base * round(x/base)

    def get_sound(output,as_list=False):
        output = int(output)
        path = f'sounds/{layer}{output}/'
        sounds = os.listdir(path)
        if len(sounds) > 0:
            if as_list:
                return(f'{sounds}') 
            sound = random.randrange(0, len(sounds))
            return(f'{path}{sounds[sound]}') 

    while 1:
        try:
            #serialPort.flush()
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

                    '''
                    for i, x in enumerate(output):
                        output[i] = myround(x,10)

                    if output != prev_output:
                        print(output)
                        prev_output = output
                        volume.change_volume(output)
                    '''

                    update = False
                    for _,i in enumerate(output):
                        i = int(i)
                        if i > prev_output[_] + 1 or i < prev_output[_] - 1:
                            update = True
                            
                    if update:
                        print(output)
                        prev_output = output
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
                            P.kill_all_sound()
                            volume.get_window()
                        else:
                            print('layer:',layer)
                            sounds = []
                            for i in range(0,5):
                                sounds.append(get_sound(i,True))
                            print(sounds)

                    else: # if not the last 4 buttons then:
                        s=get_sound(output)
                        P.play_sound(s) 


                # this code gets current voice mode and sends that to arduino
                '''
                voice_mode = p.get_voice()
                print(voice_mode)
                serialPort.write(str(voice_mode).encode()+b'\n')
                '''
        except UnicodeDecodeError:
            print('oop')

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
        for i in range(0,6):
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
