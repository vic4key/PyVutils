# https://learn.microsoft.com/en-us/windows/win32/api/endpointvolume/

from ctypes import cast, POINTER

class Speaker:
    '''System Speaker
    '''
    def __init__(self):
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        self.m_devices = AudioUtilities.GetSpeakers()
        self.m_interface = self.m_devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.m_speaker = cast(self.m_interface, POINTER(IAudioEndpointVolume))

    def __del__(self):
        pass # self.m_devices.Deactivate(self.m_interface)

    def set_volume_level(self, value: int):
        assert value >= 0 and value <= 100, "Volume level must be between 0 and 100"
        self.m_speaker.SetMasterVolumeLevelScalar(value / 100, None)

    def get_volume_level(self) -> int:
        return int(self.m_speaker.GetMasterVolumeLevelScalar() * 100)

    def muted(self) -> bool:
        return self.m_speaker.GetMute()

    def mute(self):
        self.m_speaker.SetMute(True, None)

    def unmute(self):
        self.m_speaker.SetMute(False, None)

    def toggle(self):
        self.m_speaker.SetMute(not self.muted(), None)
