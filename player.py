import pulsectl
import threading
import os

pulse = pulsectl.Pulse('my-client-name')

VIRT_MIC_MONITOR = 'PogXlr.monitor'
VIRT_MIC= 'PogXlr'

def get_default_mic():
    for mic in pulse.source_list():
        if pulse.server_info().default_source_name in mic.name:
            return(mic.name)

def get_default_speaker():
        return(pulse.server_info().default_sink_name)

DEFAULT_SPEAKER = get_default_speaker()
#print(DEFAULT_SPEAKER)
DEFAULT_MIC = get_default_mic()

class player:
    def __init__(self,default_speaker = DEFAULT_SPEAKER, default_mic = DEFAULT_MIC, virt_mic = VIRT_MIC):
        os.system(f'pacmd load-module module-loopback source={default_mic} sink={virt_mic}')
        self.default_speaker = default_speaker
        self.default_mic = default_mic
        self.virt_mic = virt_mic
        self.players = []

    def mute_mic(self,mute):
        os.system(f'pacmd set-source-mute {self.default_mic} {mute}')

    def play_sound(self, sound):
        self.sound = sound

        def play(player_id, sound):
            print(f'playing {self.sound}')
            self.mute_mic(1)
            os.system(f'paplay {self.sound} -d {self.virt_mic} & paplay {self.sound} -d {self.default_speaker}')
            self.players.remove(player_id)
            if len(self.players) == 0:
                self.mute_mic(0)

        self.player_id = len(self.players)
        t = threading.Thread(target = play, args = (self.player_id,self.sound,))
        self.players.append(self.player_id)
        t.start()

if __name__ == '__main__':
    _player = player(DEFAULT_SPEAKER, DEFAULT_MIC, VIRT_MIC)
    _player.play_sound('bruh.wav')


