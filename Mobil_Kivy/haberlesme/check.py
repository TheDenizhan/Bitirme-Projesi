import sounddevice as sd

# Define the recording parameters
duration = 5  # duration in seconds
sample_rate = 44100  # sample rate in Hz
channels = 2  # number of channels (stereo)

# Query devices to get their capabilities and indexes
print(sd.query_devices())

# Specify the index of the device you want to use
device_index = 1  # Adjust this according to the output of query_devices()

# Record audio with the specified device
try:
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels, device=device_index)
    sd.wait()  # Wait until recording is finished
    print("Recording complete.")
except Exception as e:
    print(f"Failed to record audio: {e}")
