from pulsectl import Pulse, PulseVolumeInfo
import os
import time
import subprocess

CLIENT='dummy-client'

links = []

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
    #return(compare_client(window_name,window_pid))
    return({'name':window_name, 'pid':window_pid})

# list links
def ll():
    print('LL----------')
    for i in links:
        if i != None:
            #print(i, i.volume,', ',i.proplist['application.process.binary'].lower())
            print(i)
        else:
            pass
            #print('None')
    print('ll##########')

def main():
    for i in range(0,4):
        links.append(None)

    print(links)
    
def link_client(key,client=None):
    client = get_window()

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
    print(ll())
    
def change_volume(vol):
    for i, link in enumerate(links):
        if link != None:
            with Pulse(CLIENT) as pulse:
                # enum all pulse outputs
                for cl in pulse.sink_input_list():
                    #print(link['name'].lower(),cl.proplist['application.process.binary'].lower())
                    #print(int(link['pid']),cl.proplist['application.process.id'])
                    if link['name'].lower() in cl.proplist['application.process.binary'].lower():
                        pulse.volume_set_all_chans(cl, (int(vol[i])/100))
                    #if (int(link['pid']) == int(cl.proplist['application.process.id'])):
                    #    pulse.volume_set_all_chans(cl, (int(vol[i])/100))




    

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
