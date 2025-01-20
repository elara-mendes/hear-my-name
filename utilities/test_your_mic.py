import sounddevice as sd

fs = 16000  # Samplerate
duration = 5  # 5 seconds

# Record audio
audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')

# Wait till finish
sd.wait()

print(audio_data)  # Show if your mic has song
