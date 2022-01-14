import pulsectl
import threading
import os
import signal
import subprocess

pulse = pulsectl.Pulse('my-client-name')

SOUND_BOARD= 'SoundBoard'
VIRT_MIC = 'VirtMic'
MIXED_SINK= 'MixedSink'

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
            sound_board = SOUND_BOARD):

        #os.system(f'pacmd load-module module-loopback source={default_mic} sink={sound_board}')
        #os.system(f'pacmd load-module module-loopback source={default_mic} sink={virt_mic}')
        
        # sox -t pulseaudio VirtMic -t pulseaudio MixedSink pitch -800

        # needs the .monitor at the end since its a source (pacmd list-sources)
        # pacmd load-module module-loopback source=SoundBoard.monitor sink=MixedSink
        #os.system(f'pacmd load-module module-loopback source={sound_board}.monitor sink={mixed_sink}')
        
        #os.system(f'sox -t pulseaudio {default_mic} -t pulseaudio MixedSink pitch 0')
        #os.system(f'sox -t pulseaudio {sound_board}.monitor -t pulseaudio MixedSink pitch 0')

  
        self.proc = subprocess.Popen(f'sox -t pulseaudio {sound_board}.monitor -t pulseaudio MixedSink pitch 0', 
                shell=True, 
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT)

        self.proc = subprocess.Popen(f'bash -c "exec -a FunnyMic sox -t pulseaudio {default_mic} -t pulseaudio MixedSink pitch 0"', 
                shell=True, 
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.STDOUT)
        
        
        self.default_speaker = default_speaker
        self.default_mic = default_mic
        self.sound_board = sound_board
        self.players = []

        self.voices = [
                f'bash -c "exec -a FunnyMic sox -t pulseaudio {self.default_mic} -t pulseaudio MixedSink pitch 0"',
                f'bash -c "exec -a FunnyMic sox -t pulseaudio {self.default_mic} -t pulseaudio MixedSink pitch -500"',
                f'bash -c "exec -a FunnyMic sox -t pulseaudio {self.default_mic} -t pulseaudio MixedSink pitch 500"',

                f'bash -c "exec -a FunnyMic sox -t pulseaudio {self.default_mic} -t pulseaudio MixedSink reverb 100"',
                ]
        
        self.voice = 0


    def update_bind_default_mic(self):
        os.system(f'pkill -f FunnyMic')
        # echo and reverb instead of pitch
        self.voice += 1
        if self.voice >= len(self.voices): self.voice = 0
        print(self.voices[self.voice])
        self.proc = subprocess.Popen(self.voices[self.voice], 
                shell=True, 
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.STDOUT)


    def mute_mic(self,mute):
        os.system(f'pacmd set-source-mute {self.default_mic} {mute}')

    def play_sound(self, sound):
        self.sound = sound

        def play(player_id, sound):
            print(f'playing {self.sound}')
            self.mute_mic(1)
            os.system(f'paplay {self.sound} -d {self.sound_board} & paplay {self.sound} -d {self.default_speaker}')
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


