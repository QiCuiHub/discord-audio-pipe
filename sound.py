import discord
import sounddevice as sd
from pprint import pformat

DEFAULT = 0
sd.default.channels = 2
sd.default.dtype = "int16"
sd.default.latency = "low"
sd.default.samplerate = 48000


class PCMStream(discord.AudioSource):
    def __init__(self):
        discord.AudioSource.__init__(self)
        self.stream = None

        # Discord reads 20 ms worth of audio at a time (20 ms * 50 == 1000 ms == 1 sec)
        self.frames = int(sd.default.samplerate / 50)

    def read(self):
        if self.stream is None:
            return

        data = self.stream.read(self.frames)[0]

        # convert to pcm format
        return bytes(data)

    def change_device(self, num):
        if self.stream is not None:
            self.stream.stop()
            self.stream.close()

        self.stream = sd.RawInputStream(device=num)
        self.stream.start()


class DeviceNotFoundError(Exception):
    def __init__(self):
        self.devices = sd.query_devices()
        self.host_apis = sd.query_hostapis()
        super().__init__("No Devices Found")

    def __str__(self):
        return (
            f"Devices \n"
            f"{self.devices} \n "
            f"Host APIs \n"
            f"{pformat(self.host_apis)}"
        )


def query_devices():
    options = {
        device.get("name"): index
        for index, device in enumerate(sd.query_devices())
        if (device.get("max_input_channels") > 0 and device.get("hostapi") == DEFAULT)
    }

    if not options:
        raise DeviceNotFoundError()

    return options
