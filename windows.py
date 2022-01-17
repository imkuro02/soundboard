from pulsectl import Pulse, PulseVolumeInfo
import os
import time
import subprocess

client='dummy-client'

def get_window():
    with Pulse(client) as pulse:
        # loop through all sink inputs and set the volumes.
        # Weird fact: the sink input won't enumerate unless it is outputing audio
        window_pid = subprocess.check_output('xdotool getwindowfocus getwindowpid', shell=True).decode('utf-8')
        window_id = subprocess.check_output(f'xdotool search --pid {window_pid}', shell=True).decode('utf-8').split()
        print(window_id)
        window_name = subprocess.check_output(f'xdotool getwindowname {window_id[0]}',shell=True).decode('utf-8').replace('\n','')
        print(window_name)

        for i,cl in enumerate(pulse.sink_input_list()):
            print(f'\"{window_name.lower()}\"',f'\"{cl.proplist["application.process.binary"].lower()}\"') 
            #print(cl.index, cl.proplist['application.process.binary'],cl.volume)
            if window_name.lower() in cl.proplist['application.process.binary'].lower():
                print('>',cl.index, cl.proplist['application.process.binary'],cl.volume)

        
if __name__ == '__main__':
    time.sleep(1)
    # get pid of focused window 
    get_window()

