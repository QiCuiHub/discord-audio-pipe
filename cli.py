import sound
import discord
import logging

async def connect(bot, stream, device_id, channel_id, token):
    try:
        print('Connecting...')
        await bot.wait_until_ready()
        print(f'Logged in as {bot.user.name}')

        selected = None

        for guild in bot.guilds:
            for channel in guild.channels:
                if channel_id == channel.id:
                    selected = channel

        stream.change_device(device_id)        
        voice = await selected.connect()
        voice.play(discord.PCMAudio(stream))

        print(f'Playing audio in {selected.name}')

    except:
        logging.exception('Error on cli connect')

async def query(bot, token):
    await bot.login(token)

    async for guild in bot.fetch_guilds(limit=150):
        print(guild.id, guild.name)
        channels = await guild.fetch_channels()
        
        for channel in channels:
            print('\t', channel.id, channel.name)

    await bot.logout()