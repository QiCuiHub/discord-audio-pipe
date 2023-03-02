import os
import importlib.util
            
spec = importlib.util.find_spec('sounddevice')
site_packages = os.path.dirname(spec.origin)
binary_folder = os.path.join("_sounddevice_data", "portaudio-binaries")

datas = [(os.path.join(site_packages, binary_folder), binary_folder)]
