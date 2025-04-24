import sys
from pydub import AudioSegment

def ExtractVoice(project ,vid):
    vocals = project+'/'+vid+'/audio.wav'
    audio = AudioSegment.from_file(vid)
    audio.export(vocals, format='wav')
    return vocals

        