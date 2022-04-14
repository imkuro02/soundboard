from pulsectl import Pulse, PulseVolumeInfo
import os
import time
import subprocess

CLIENT='my-client-name'
CONFIG='settings.txt'

links = [[],[],[],[]]

def get_window():
    # get cur window info
    print('\n######################')
    print('compare name to these:\n')
    with Pulse(CLIENT) as pulse:
        for i, cl in enumerate(pulse.sink_input_list()):
            if 'application.process.binary' in cl.proplist:
                print(cl.proplist['application.process.binary'])
    print('')
    window_pid = subprocess.check_output('xdotool getwindowfocus getwindowpid', shell=True).decode('utf-8')
    window_id = subprocess.check_output(f'xdotool search --pid {window_pid}', shell=True).decode('utf-8').split()
    window_name = subprocess.check_output(f'xdotool getwindowname {window_id[0]}',shell=True).decode('utf-8').replace('\n','')
    print(f'window_name: "{window_name}", pid: {window_pid}')
    print('\n######################\n')

def change_volume(vol):
    try:
        with open(CONFIG) as config:
            content = config.readlines()
            for i in range(0,4):
                links[i] = content[i].replace('\n','').split(',')
                #print(link)
    except FileNotFoundError:
        print(f'{CONFIG}, not found probably just written')

    for i, link in enumerate(links):
        if link != ['']:
            with Pulse(CLIENT) as pulse:
                # enum all pulse outputs
                for cl in pulse.sink_input_list():
                    #print(link['name'].lower(),cl.proplist['application.process.binary'].lower())
                    #print(int(link['pid']),cl.proplist['application.process.id'])
                    for source in link:
                        # check if app has a process.binary
                        if 'application.process.binary' in cl.proplist:
                            if source.lower() in cl.proplist['application.process.binary'].lower():
                                try:
                                    pulse.volume_set_all_chans(cl, (int(vol[i])/100))
                                except Exception as e:
                                    print(e)
