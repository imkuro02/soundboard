import pulsectl
import subprocess
import sys

def notify_send(message):
    subprocess.call(["notify-send", "PulseAudio App Sink Switcher", message])

def fail(message):
    print(message, file=sys.stderr)
    notify_send(message)
    exit(1)

if len(sys.argv) < 2:
    print("Usage: {} <toggle sink name>", file=sys.stderr)
    exit(1)

toggle_output_sink_name = sys.argv[1]

try:
    active_window_id = int(subprocess.getoutput("xdotool getactivewindow"))
    foreground_pid = int(subprocess.getoutput("xdotool getwindowpid {}".format(active_window_id)))
except Exception:
    fail("Can't get PID of active window")

try:
    application_name = subprocess.getoutput("xdotool getwindowname {}".format(active_window_id))
except Exception:
    application_name = None

pulse = pulsectl.Pulse("app-sink-switcher")

default_output_sink_name = pulse.server_info().default_sink_name
default_output_sink = pulse.get_sink_by_name(default_output_sink_name).index

try:
    toggle_output_sink = pulse.get_sink_by_name(toggle_output_sink_name).index
except pulsectl.PulseIndexError:
    fail("Sink '{}' not found!".format(toggle_output_sink_name))

input_sink = None
current_output_sink = None

for sink in pulse.sink_input_list():
    if "application.process.id" in sink.proplist and int(sink.proplist["application.process.id"]) == foreground_pid:
        input_sink = sink.index
        current_output_sink = sink.sink
        break

if input_sink is None:
    fail("Foreground application {} (PID {}) is not connected to PulseAudio!".format(application_name, foreground_pid))

# Toggle between default and specified sink
if current_output_sink == default_output_sink:
    new_output_sink_name = toggle_output_sink_name
    new_output_sink = toggle_output_sink
else:
    new_output_sink_name = default_output_sink_name
    new_output_sink = default_output_sink

print("Connecting application {} (PID {}) to sink {} (input sink {} -> output sink {})".format(application_name, foreground_pid, new_output_sink_name, input_sink, new_output_sink))
pulse.sink_input_move(input_sink, new_output_sink)

notify_send("Application audio output of {} switched to {}".format(application_name, new_output_sink_name))
