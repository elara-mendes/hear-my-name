import os
import sounddevice
import queue
from vosk import Model, KaldiRecognizer


MODEL_PATH = "model"
SAMPLERATE = 16000

if not os.path.exists(MODEL_PATH):
    print("Verify the folder path.")
else:
    print("Pass!")  # To know if the folder exists

model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, SAMPLERATE)
audio_queue = queue.Queue()


def callback(indata, frames, time, status):
    if status:
        print(f"Status: {status}")
    audio_queue.put(bytes(indata))


# Input configuration
with sounddevice.RawInputStream(samplerate=SAMPLERATE, dtype="int16", channels=1, callback=callback,
                                blocksize=8000):
    print("Speak something...")

    while True:
        data = audio_queue.get()  # Get the audio from queue
        if recognizer.AcceptWaveform(data):
            print("Recognized:", recognizer.Result())
        else:
            print("Partial:", recognizer.PartialResult())
