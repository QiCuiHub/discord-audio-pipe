import numpy as np
import sounddevice as sd


sd.default.channels = 2, 2
sd.default.dtype = 'int16'
sd.default.latency = 'low'
sd.default.samplerate = 48000


class PCMStream:
    def __init__(self):
        self.ch = sd.default.channels[0]
        self.api = None
        self.device = None
        self.stream = None

    def read(self, num_bytes):
        # 2 bytes per channel
        frames = int(num_bytes / (2 * self.ch))
        data = self.stream.read(frames)[0]

        # convert to pcm format
        return data.tobytes()

    def change_device(self, num):
        self.device = num
    
        if (self.stream is not None):
            self.stream.stop()
            self.stream.close()

        self.stream = sd.InputStream(
            device=num, 
            channels=sd.query_devices(num).get('max_input_channels'), 
            samplerate=sd.query_devices(num).get('default_samplerate')
        )

        self.stream.start()
        
    def change_api(self, num):
        self.api = num
        
        if (self.stream is not None):
            self.stream.stop()
            self.stream.close()

            self.stream = sd.InputStream(
                device=self.device,
                channels=sd.query_devices(num).get('max_input_channels'), 
                samplerate=sd.query_devices(num).get('default_samplerate')
            )
            
            self.stream.start()

    def query_apis(self):
        options = {}
        
        for idx, item in enumerate(sd.query_hostapis()):
            options[item.get('name')] = idx

        return options

    def query_devices(self):
        options = {}
        
        for idx, item in enumerate(sd.query_devices()):
            # pip version only supports MME api
            if (item.get('max_input_channels') > 0 and item.get('hostapi') == self.api):
                options[item.get('name')] = idx

        return options
