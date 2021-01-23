import sys
import sound
import discord
import logging


async def connect(bot, device_id, channel_id):
    try:
        print("Connecting...")
        await bot.wait_until_ready()
        print(f"Logged in as {bot.user.name}")

        stream = sound.PCMStream()
        channel = bot.get_channel(channel_id)
        stream.change_device(device_id)

        voice = await channel.connect()
        voice.play(discord.PCMAudio(stream))

        print(f"Playing audio in {channel.name}")

    except Exception:
        logging.exception("Error on cli connect")
        sys.exit(1)


async def query(bot, token):
    await bot.login(token)

    async for guild in bot.fetch_guilds(limit=150):
        print(guild.id, guild.name)
        channels = await guild.fetch_channels()

        for channel in channels:
            print("\t", channel.id, channel.name)

    await bot.logout()
