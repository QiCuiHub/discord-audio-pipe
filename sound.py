import numpy as np
import sounddevice as sd

sd.default.dtype = 'int16'
sd.default.latency = 'low'
sd.default.samplerate = 48000

class PCMStream:
    def __init__(self):
        self.ch = 2
        self.sr = 48000
        self.stream = None
        
    def read(self, num_bytes):
        # 2 bytes per channel
        frames = int(num_bytes / (2 * self.ch))
        data = self.stream.read(frames)[0]

        # convert to pcm format
        return data.tobytes()

    def change_device(self, num):
        if (self.stream is not None):
            self.stream.stop()
            self.stream.close()
    
        self.ch = sd.query_devices(num).get('max_input_channels')
        self.sr = sd.query_devices(num).get('default_samplerate')
        self.stream = sd.InputStream(device=num, channels=self.ch, samplerate=self.sr)
        self.stream.start()


def query_devices():
    index = 0
    options = {}
    
    for item in sd.query_devices():
        # pip version only supports MME api
        if (item.get('max_input_channels') > 0 and item.get('hostapi') == 3):
            options[item.get('name')] = index
                
        index += 1

    return options
