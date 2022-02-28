import os
import serial
import threading
import serial
import random
from time import sleep
import player
import volume

def reload_player(p):
    for i in range(0,10):
        sleep(3)
        p.cleanup(False) # if you dont say False here, module-null-sink will get removed
        p.init_sox()
        print('reload: ',i)
    print('fully reloaded')


def main():
    p = player.player()
    p.init_modules()
    p.init_sox()

    volume.main()

    try:
        print('ready')

        # reloads a couple of times to make sure sox isnt slow
        # paused to check that if i wait before turning the software on after reboot it will 
        # act normal
        reloader = threading.Thread(target = reload_player, args=(p,))
        reloader.setDaemon(True)
        reloader.start()

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
                
                    '''
                    index = random.randint(1, 11)
                    if '1' in output : p.play_sound(f'sounds/moans/{index}.wav') 
                    RAND = random.randint(-1000, 1000)
                    #if '2' in output : p.play_sound(f'moans/{index}.wav') 
                    if '2' in output : 
                        p.update_bind_default_mic() 
                    '''
                    # last 4 buttons are volume slider links
                    if int(output)>=6:
                        if '6' in output:
                            volume.link_client(0)
                        if '7' in output:
                            volume.link_client(1)
                        if '8' in output:
                            volume.link_client(2)               
                        if '9' in output:
                            volume.link_client(3)               
                    else: # if not the last 4 buttons then:
                        if '0' in output: # if 0, do mic change
                            p.update_bind_default_mic() 
                        else: # if not 0, play sound from folder
                            output = int(output)
                            path = f'sounds/{output}/'
                            sounds = os.listdir(path)
                            if len(sounds) > 0:
                                print(sounds)
                                sound = random.randrange(0, len(sounds))
                                p.play_sound(f'{path}{sounds[sound]}') 


                # this code gets current voice mode and sends that to arduino
                '''
                voice_mode = p.get_voice()
                print(voice_mode)
                serialPort.write(str(voice_mode).encode()+b'\n')
                '''
    finally:
        p.cleanup()


if __name__ == '__main__':


    # ./create_sink.sh

    main()

    # pulsaudio -k
    #play_sound()

