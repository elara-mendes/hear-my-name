import os
import sounddevice
import queue
import json
from vosk import Model, KaldiRecognizer


MODEL_PATH = "model"
SAMPLERATE = 16000
OUTPUT_FILE = "output.txt"

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
            result_json = recognizer.Result()
            result_dict = json.loads(result_json)
            recognized_text = result_dict.get("text", "")

            if recognized_text: # Recognized text from JSON
                print("Recognized:", recognized_text)
                with open(OUTPUT_FILE, "a") as output_text:
                    output_text.write(recognized_text + "\n")
            if "Nat".lower() in recognized_text.lower():
                print("You are my beloved!")
        # else:
        #     partial_json = recognizer.PartialResult()  # Partial result from JSON
        #     partial_dict = json.loads(partial_json)
        #     partial_text = partial_dict.get("partial", "")
        #     print("Partial:", partial_text)
