import sound
import tkinter as tk

class UI():
    def __init__(self, exit_protocol):
        self.root = tk.Tk()
        self.root.title("Bot")

        self.cred = tk.Label(self.root, text='Connecting...', fg='black')
        self.cred.grid(row=0, column=0, columnspan=2, sticky='W')
        
        tk.Label(self.root, text='Device', fg='black').grid(row=1, column=0)
        tk.Label(self.root, text='Server', fg='black').grid(row=1, column=1)
        tk.Label(self.root, text='Channel', fg='black').grid(row=1, column=2)

        device_options = sound.query_devices()
        dv = tk.StringVar(self.root)
        dv.trace("w", lambda *args: self.change_device(device_options, dv))
        dv.set(device_options.get(0))
        device = tk.OptionMenu(self.root, dv, *device_options)
        device.grid(row=2, column=0)

        sv = tk.StringVar(self.root)
        sv.set('None')
        self.server = tk.OptionMenu(self.root, sv, 'None')
        self.server.grid(row=2, column=1)

        cv = tk.StringVar(self.root)
        cv.set('None')
        self.channel = tk.OptionMenu(self.root, cv, 'None')
        self.channel.grid(row=2, column=2)

        self.exit_protocol = exit_protocol
        self.root.protocol("WM_DELETE_WINDOW", self.exit)

    def exit(self):
        self.exit_protocol()
        self.root.destroy()

    def change_device(self, options, dv):
        print (options.get(dv.get()))

    def set_cred(self, username):
        self.cred.config(text='Logged in as: ' + username)
        
    def set_channels(self, channels):
        menu = self.channel['menu']
        for string in channels:
            menu.add_command(label=string, command=lambda value=string: self.channel.set(value))

    def set_servers(self, servers):
        menu = self.server['menu']
        for string in servers:
            menu.add_command(label=string, command=lambda value=string: self.server.set(value))

    
