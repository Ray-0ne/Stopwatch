import wave
import struct
import math

with wave.open("alarm.wav", "w") as wav_file:
    params = (1, 2, 44100, 0, 'NONE', 'not compressed')
    wav_file.setparams(params)
    volume = 32767
    freq = 440.0
    duration = 1.0
    for i in range(int(44100 * duration)):
        value = int(volume * math.sin(2 * math.pi * freq * i / 44100))
        wav_file.writeframes(struct.pack('h', value))
