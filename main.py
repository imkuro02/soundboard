import os
import pulsectl

pulse = pulsectl.Pulse('my-client-name')

VIRT_MIC = 'PogXlr.monitor'
VIRT_MIC_MONITOR = 'PogXlr'

def change_mic(mic):
    os.system(f'pacmd set-default-source {mic}')

def get_default_mic():
    return(pulse.server_info().default_source_name)

def play_sound():
    sound = 'bruh.wav'
    os.system(f'paplay {sound} -d {VIRT_MIC_MONITOR}')

def main():
    '''
    print(get_default_mic())
    for i in pulse.sink_list():
        print(i)
    '''
    for i in pulse.source_list():
        if get_default_mic() in i.name:
            default_mic = i

    for i in pulse.source_list(): # Input Devices
        print(i)

    '''
    for i in pulse.sink_list():
        if VIRT_MIC in i.name:
            new_mic = i.index
    '''

    change_mic(VIRT_MIC)
    play_sound()
    print('')
    print(default_mic.name)
    change_mic(default_mic.name)



if __name__ == '__main__':
    main()
    #play_sound()

