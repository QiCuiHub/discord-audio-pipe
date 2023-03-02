import os
import importlib.util
            
spec = importlib.util.find_spec('discord')
module_dir = os.path.dirname(spec.origin)

datas = [(os.path.join(module_dir, 'bin/libopus-0.x64.dll'), './discord/bin/')]
