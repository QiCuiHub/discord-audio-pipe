import numpy as np
import sounddevice as sd

MME = 0
sd.default.channels = 2
sd.default.dtype = 'int16'
sd.default.latency = 'low'
sd.default.samplerate = 48000

class PCMStream:
    def __init__(self):
        self.stream = None
        
    def read(self, num_bytes):
        # frame is 4 bytes
        frames = int(num_bytes / 4)
        data = self.stream.read(frames)[0]

        # convert to pcm format
        return data.tobytes()

    def change_device(self, num):
        if (self.stream is not None):
            self.stream.stop()
            self.stream.close()

        self.stream = sd.InputStream(device=num)
        self.stream.start()

def query_devices():
    index = 0
    options = {}

    for item in sd.query_devices():
        # pip version only supports MME api
        if (item.get('max_input_channels') > 0 and item.get('hostapi') == MME):
            options[item.get('name')] = index

        index += 1

    return options
