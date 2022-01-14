from pulsectl import Pulse, PulseVolumeInfo
import os
import time
import subprocess

client='dummy-client'

def allAppVolumes(level):
    with Pulse(client) as pulse:
      # loop through all sink inputs and set the volumes.
      # Weird fact: the sink input won't enumerate unless it is outputing audio
      pid = subprocess.check_output('xdotool getwindowfocus getwindowpid', shell=True)
      winid = subprocess.check_output('xdotool getactivewindow', shell=True)
      print(winid)
      pid = int(pid)
      print(pid)
      for i,cl in enumerate(pulse.sink_input_list()):
        cl_pid = int(cl.proplist['application.process.id'])
        print(pid, cl_pid)
        print(cl.proplist)

        if pid == cl_pid:
            print('match!')
            print(cl.proplist)
            print(cl.index, cl.proplist['application.process.binary'])
        
if __name__ == '__main__':
    time.sleep(1)
    # get pid of focused window 
    allAppVolumes(1)

