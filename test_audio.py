import sounddevice as sd
import numpy as np

print("Audio Device Test")
print("=" * 50)

devices = sd.query_devices()
print(f"\nFound {len(devices)} devices:\n")

for i, device in enumerate(devices):
    print(f"[{i}] {device['name']}")
    print(f"    Input: {device['max_input_channels']}, Output: {device['max_output_channels']}")
    print()

print("Testing microphone input...")
try:
    duration = 3
    fs = 16000
    print(f"Recording for {duration} seconds...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()
    print("✓ Microphone working!")
    
    print(f"Playback test...")
    sd.play(recording, fs)
    sd.wait()
    print("✓ Speakers working!")
except Exception as e:
    print(f"✗ Error: {e}")
    print("Check System Preferences > Security & Privacy > Microphone")
