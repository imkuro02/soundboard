import pulsectl
import threading
import os
import signal
import atexit

pulse = pulsectl.Pulse('my-client-name')

SOUND_BOARD= 'SoundBoard'
VIRT_MIC = 'VirtMic'
MIXED_SINK= 'MixedSink'
PAPLAY_NAME= 'soundboardPaplay'

def get_default_mic():
    for mic in pulse.source_list():
        if pulse.server_info().default_source_name in mic.name:
            return(mic.name)

def get_default_speaker():
        return(pulse.server_info().default_sink_name)

DEFAULT_SPEAKER = get_default_speaker()
#print(DEFAULT_SPEAKER)
DEFAULT_MIC = get_default_mic()

def bind_sound_board(default_mic,sound_board):
    os.system(f'sox -t pulseaudio {sound_board}.monitor -t pulseaudio MixedSink pitch 0')

def bind_default_mic(default_mic,sound_board,val=0):
    os.system(f'sox -t pulseaudio {default_mic} -t pulseaudio MixedSink pitch {val}')
    print('VAL ',val)


class player:
    def __init__(self, 
            mixed_sink = MIXED_SINK, 
            default_speaker = DEFAULT_SPEAKER, 
            default_mic = DEFAULT_MIC, 
            virt_mic = VIRT_MIC, 
            paplay_name = PAPLAY_NAME, 
            sound_board = SOUND_BOARD):
       
        # sox -t pulseaudio VirtMic -t pulseaudio MixedSink pitch -800

        # needs the .monitor at the end since its a source (pacmd list-sources)
        # pacmd load-module module-loopback source=SoundBoard.monitor sink=MixedSink
        #os.system(f'pacmd load-module module-loopback source={sound_board}.monitor sink={mixed_sink}')
        
        #os.system(f'sox -t pulseaudio {default_mic} -t pulseaudio MixedSink pitch 0')
        #os.system(f'sox -t pulseaudio {sound_board}.monitor -t pulseaudio MixedSink pitch 0')

    
       
        
        self.default_speaker = default_speaker
        self.default_mic = default_mic
        self.sound_board = sound_board
        self.paplay_name = paplay_name
        self.players = []
        self.modules = []

    def cleanup(self,full_cleanup=True):
        # this will bascially always trigger unless specifically told NOT TO with "False" 
        if full_cleanup: 
            for i in self.modules:
                print(i)
                os.popen(f'pactl unload-module {i}')

    def init_modules(self):
        self.modules.append(os.popen('pactl load-module module-null-sink sink_name=SoundBoard').read())
        #self.modules.append(os.popen('pactl load-module module-null-sink sink_name=MixedSink').read())
        self.modules.append(os.popen(f'pactl load-module module-loopback source={DEFAULT_MIC} sink={SOUND_BOARD}').read())
        #self.modules.append(os.popen(f'pactl load-module module-loopback source={DEFAULT_MIC} sink={VIRT_MIC}').read())
 
        for i in self.modules:
            print('module : ',i)

    def mute_mic(self,mute):
        os.system(f'pacmd set-source-mute {self.default_mic} {mute}')

    def kill_all_sound(self):
       pids = os.popen('ps aux | grep -i soundboardPaplay | awk \'{print $2}\'').read() # get all soundplayers owned by this program
       pids = str(pids).split()
       for pid in pids:
           try: 
               pid = int(str(pid))
           except ValueError:
                return

           try:
                os.kill(pid,signal.SIGKILL)
           except ProcessLookupError:
                # this pid cant be killed, who cares tho
                pass    
           except PermissionError:
                pass
           
    def play_sound(self, sound):
        self.sound = sound

        def play(player_id, sound):
            print(f'playing {self.sound}')
            self.mute_mic(1) # mute mic

            os.system(f"bash -c 'exec -a {self.paplay_name} paplay {self.sound} -d {self.sound_board}&'")# read man page for vol
            os.system(f"bash -c 'exec -a {self.paplay_name} paplay {self.sound} -d {self.default_speaker} --volume 25536'")# read man page for vol

            self.players.remove(player_id)
           
            if len(self.players) == 0:
                self.mute_mic(0)

        self.player_id = len(self.players)
        t = threading.Thread(target = play, args = (self.player_id,self.sound,))
        self.players.append(self.player_id)
        t.start()

if __name__ == '__main__':
    _player = player(DEFAULT_SPEAKER, DEFAULT_MIC, VIRT_MIC, SOUND_BOARD)
    _player.play_sound('bruh.wav')


