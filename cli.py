import sound
import discord

async def connect(bot, device, server, channel):
    stream = sound.PCMStream()
    stream.change_device(device)

    guild = discord.utils.find(server, bot.guilds)
    channel = discord.utils.find(channel, guilds.channels)

    voice = await channel.connect()
    voice.play(discord.PCMAudio(stream))
    
async def disconnect(bot):
    bot._closed = True

    for voice in bot.voice_clients:
        try:
            await voice.disconnect()
        except Exception:
            pass

    await bot.ws.close()