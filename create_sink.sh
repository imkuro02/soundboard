
pacmd load-module module-null-sink sink_name=SoundBoard
pacmd update-sink-proplist SoundBoard device.description=SoundBoard

pacmd load-module module-null-sink sink_name=MixedSink
pacmd update-sink-proplist MixedSink device.description=MixedSink

