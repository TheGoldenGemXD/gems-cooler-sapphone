# win32com might not be necessary here
# pyttsx uses comtypes but it still depends on win32com ???
from dataclasses import field

from pydantic import BaseModel, Field
import win32com.client
import comtypes.client
try:
    from comtypes.gen import SpeechLib
except ImportError:
    # Generate the SpeechLib lib and any associated files
    engine = comtypes.client.CreateObject("SAPI.SpVoice")
    stream = comtypes.client.CreateObject("SAPI.SpFileStream")
    from comtypes.gen import SpeechLib

class VoiceModel(BaseModel):
    voice: str = Field(default=r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0", title="Voice")
    rate: float = Field(default=0, ge=-10, le=10, title="Rate")
class ConfigModel(BaseModel):
    voice: VoiceModel = Field(default_factory=VoiceModel, title="Voice")

# list of voice token attributes for testing
sapi_attributes = ["Name", "Gender", "Age", "Language", "Vendor"]


class SapphoneEngine:
    ConfigModel = ConfigModel
    def __init__(self, config):
        self.config = config
        self.tts = win32com.client.Dispatch("SAPI.SpVoice")
        for i in self.tts.GetVoices():
            if i.Id == self.config.voice.voice:
                self.tts.Voice = i
        self.tts.Rate = self.config.voice.rate

    def speak_to_file(self, script, output):
        output_stream = win32com.client.Dispatch("SAPI.SPFileStream")
        output_stream.Open(output, SpeechLib.SSFMCreateForWrite)
        tts_stream = self.tts.AudioOutputStream
        self.tts.AudioOutputStream = output_stream
        self.tts.Speak(script)
        self.tts.AudioOutputStream = tts_stream
        output_stream.close()
