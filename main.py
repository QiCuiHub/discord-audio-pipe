import ui
import sound
import asyncio
import discord
from discord.ext import commands

async def run_tk(root, interval=0.05):
    try:
        while True:
            root.update()
            await asyncio.sleep(interval)
    except ui.tk.TclError as e:
        return
        
async def ready(bot, bot_ui):
    await bot.wait_until_ready()

    #channel = bot.get_channel('401578097511759897')
    #voice = await bot.join_voice_channel(channel)

    #player = voice.create_stream_player(PCMStream())
    #player.start()

    bot_ui.set_cred(bot.user.name)
    
    servers = [server for server in bot.servers]
    bot_ui.set_servers(servers)
    channels = [channel for channel in bot.get_all_channels()]
    bot_ui.set_channels(channels)

    #channel = discord.utils.find(lambda c: c.name == 'General' and c.type == 'voice', bot.servers.get('bittleserver').channels)
    #if channel is not None:
        #print(channel.id)

bot = discord.Client()
bot_ui = ui.UI(lambda: asyncio.ensure_future(bot.logout()))
loop = asyncio.get_event_loop()

try:
    asyncio.ensure_future(run_tk(bot_ui.root, interval=0.05))
    asyncio.ensure_future(ready(bot, bot_ui))
    
    loop.run_until_complete(bot.start(open('token.txt', 'r').read()))
except KeyboardInterrupt:
    loop.run_until_complete(bot.logout())
finally:
    loop.close()
