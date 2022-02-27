
pactl load-module module-null-sink sink_name=SoundBoard
pactl update-sink-proplist SoundBoard device.description=SoundBoard

pactl load-module module-null-sink sink_name=MixedSink
pactl update-sink-proplist MixedSink device.description=MixedSink

