from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import ctypes

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))

def set_volume(level):
    volume.SetMasterVolumeLevelScalar(level, None)

def volume_up():
    current = volume.GetMasterVolumeLevelScalar()
    if current < 1.0:
        set_volume(min(current + 0.1, 1.0))

def volume_down():
    current = volume.GetMasterVolumeLevelScalar()
    if current > 0.0:
        set_volume(max(current - 0.1, 0.0))
