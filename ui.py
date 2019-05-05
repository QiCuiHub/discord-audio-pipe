import sound
import discord
import asyncio
import tkinter as tk

class UI():
    def __init__(self, bot):
        self.root = tk.Tk()
        self.root.title('Bot')
        
        self.bot = bot
        self.voice = None
        self.stream = sound.PCMStream()
        
        self.cred = tk.Label(self.root, text='Connecting...', fg='black')
        self.cred.grid(row=0, column=0, columnspan=2, sticky='W')
        
        tk.Label(self.root, text='Device', fg='black').grid(row=1, column=0)
        tk.Label(self.root, text='Server', fg='black').grid(row=1, column=1)
        tk.Label(self.root, text='Channel', fg='black').grid(row=1, column=2)

        device_options = sound.query_devices()
        dv = tk.StringVar(self.root)
        dv.trace('w', lambda *args: asyncio.ensure_future(self.change_device(device_options, dv)))
        dv.set(device_options.get(0))
        device = tk.OptionMenu(self.root, dv, *device_options)
        device.grid(row=2, column=0)

        self.sv = tk.StringVar(self.root)
        self.sv.trace('w', lambda *args: asyncio.ensure_future(self.change_server()))
        self.sv.set('None')
        self.server = tk.OptionMenu(self.root, self.sv, 'None')
        self.server.grid(row=2, column=1)

        self.cv = tk.StringVar(self.root)
        self.cv.trace("w", lambda *args: asyncio.ensure_future(self.change_channel()))
        self.cv.set('None')
        self.channel = tk.OptionMenu(self.root, self.cv, 'None')
        self.channel.grid(row=2, column=2)

        self.mv = tk.StringVar(self.root)
        self.mv.set('Mute')
        self.mute = tk.Button(self.root, textvariable=self.mv, command=self.toggle_mute)
        self.mute.grid(row=2, column=3, padx=5)
        
        self.root.protocol('WM_DELETE_WINDOW', self.on_exit)

    def on_exit(self):
        asyncio.ensure_future(self.bot.logout())
        self.root.destroy()

    async def change_device(self, options, dv):
        if (dv.get() != 'None'):
            if (self.voice is not None):
                self.voice.stop()
                self.stream.change_device(options.get(dv.get()))
                self.voice.play(discord.PCMAudio(self.stream))
            else:
                self.stream.change_device(options.get(dv.get()))

    async def run_tk(self, interval=0.05):
        try:
            while True:
                self.root.update()
                await asyncio.sleep(interval)
        except tk.TclError as e:
            return
        
    async def change_server(self):
        name = self.sv.get()

        if (name != 'None'):
            guild = discord.utils.find(lambda s: s.name == name, self.bot.guilds)
            channel_names = [c.name for c in guild.channels if isinstance(c, discord.VoiceChannel)]
            self.set_channels(['None'] + channel_names)    
        else:
            self.set_channels(['None'])

        if (self.voice is not None):
            await self.voice.disconnect()
            self.voice = None
        
    async def change_channel(self):
        s_name = self.sv.get()
        c_name = self.cv.get()

        if (c_name != 'None'):
            guild = discord.utils.find(lambda s: s.name == s_name, self.bot.guilds)
            channel = discord.utils.find(lambda c: c.name == c_name, guild.channels)
            
            if (self.voice is None):
                self.voice = await channel.connect()
            else:
                await self.voice.move_to(channel)

            self.voice.play(discord.PCMAudio(self.stream))
        else:
            if (self.voice is not None):
                await self.voice.disconnect()
                self.voice = None

    def set_cred(self, username):
        self.cred.config(text='Logged in as: ' + username)

    def set_servers(self, servers):
        menu = self.server['menu']

        for string in servers:
            menu.add_command(label=string, command=lambda value=string: self.sv.set(value))
            
    def set_channels(self, channels):
        menu = self.channel['menu']
        menu.delete(0, 'end')
        
        for string in channels:
            menu.add_command(label=string, command=lambda value=string: self.cv.set(value))    
    
    def toggle_mute(self):
        if (self.voice is not None):
            if (self.voice.is_playing()):
                self.voice.pause()
                self.mv.set('Resume')
            else:
                self.voice.resume()
                self.mv.set('Mute')
