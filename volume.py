from pulsectl import Pulse, PulseVolumeInfo
import os
import time
import subprocess

CLIENT='dummy-client'

links = []

class Source:
    def __init__(self, index, name, volume):
        self.index  = index
        self.name   = name 
        self.volume = volume

def compare_client(window_name,window_pid):
    with Pulse(CLIENT) as pulse:
         # enum all pulse outputs
        for i, cl in enumerate(pulse.sink_input_list()):
            if (window_name.lower() in cl.proplist['application.process.binary'].lower()):
                return(cl)
            if (int(window_pid) == int(cl.proplist['application.process.id'])):
                return(cl)

def get_window():
    # get cur window info
    window_pid = subprocess.check_output('xdotool getwindowfocus getwindowpid', shell=True).decode('utf-8')
    window_id = subprocess.check_output(f'xdotool search --pid {window_pid}', shell=True).decode('utf-8').split()
    window_name = subprocess.check_output(f'xdotool getwindowname {window_id[0]}',shell=True).decode('utf-8').replace('\n','')
    return(compare_client(window_name,window_pid))

# list links
def ll():
    print('LL----------')
    for i in links:
        if i != None:
            print(i, i.volume,', ',i.proplist['application.process.binary'].lower())
        else:
            print('None')
    print('ll##########')

def main():
    for i in range(0,4):
        links.append(None)

    print(links)
    
def link_client(key,client=None):
    if client == None:
        client = get_window()
    else:
        print('>',client)
        client = compare_client(client.proplist['application.process.binary'],client.proplist['application.process.id'])

    # check if you are overwriting a key
    for i, cl in enumerate(links):
        try:
            if client.index == cl.index:
                #print(f'overwrite {key}')
                links[i] = None
        except AttributeError:
            pass
            #print('Attribute Error :P')

    # link client to key
    links[key] = client
    
def change_volume(vol):
    for i, link in enumerate(links):
        print(link)
        if link != None:
            with Pulse(CLIENT) as pulse:
                for x in pulse.sink_input_list():
                    # if there is a link with this name, proceed
                    if link.proplist['application.process.binary'] == x.proplist['application.process.binary']:
                        # ok so, lets just relink this thing just to be safe :)
                        if link.index != x.index:
                            link_client(i,link)
                        else:
                            print(link,x)
                            pulse.volume_set_all_chans(link, (int(vol[i])/100))
    

if __name__ == '__main__':
    main()
    ll()
    time.sleep(1)
    link_client(1)
    ll()
    time.sleep(1)
    link_client(2)
    ll()
    time.sleep(1)
    link_client(3)
    ll()
    print('done')

    # get pid of focused window 
    '''
    for i in range(0,3):
        get_window()

    print('-----------------------')

    for i in sources:
        print(i.index,i.name)
    '''
