import discord
import numpy as np
import sounddevice as sd
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

sd.default.device = 1
sd.default.channels = 2
sd.default.dtype = 'int16'
sd.default.latency = 'low'
sd.default.samplerate = 48000

class PCMStream:
    def __init__(self):
        self.stream = sd.InputStream()
        self.stream.start()
        
    def read(self, num_bytes):
        # frame is 4 bytes
        frames = int(num_bytes / 4)
        data = self.stream.read(frames)[0]

        # convert to pcm format
        return data.tobytes()

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(sd.query_devices())
    
    channel = bot.get_channel('')
    voice = await bot.join_voice_channel(channel)

    player = voice.create_stream_player(PCMStream())
    player.start()

bot.run('');
