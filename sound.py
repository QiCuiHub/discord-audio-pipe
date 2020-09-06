import numpy as np
import sounddevice as sd
from pprint import pformat

DEFAULT = 0
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
        if self.stream is not None:
            self.stream.stop()
            self.stream.close()

        self.stream = sd.InputStream(device=num)
        self.stream.start()

class DeviceNotFoundError(Exception):
    def __init__(self):
        self.devices = sd.query_devices()
        self.host_apis = sd.query_hostapis()
        super().__init__('No Devices Found')

    def __str__(self):
        return f'Devices \n{self.devices} \n Host APIs \n{pformat(self.host_apis)}'

def query_devices():
    options = {
        item.get('name') : index
        for index, item in enumerate(sd.query_devices())
        if item.get('max_input_channels') > 0 and item.get('hostapi') == DEFAULT
    }

    if not options:
        raise DeviceNotFoundError()

    return options
