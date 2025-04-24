import os
import sys
import subprocess
from pydub import AudioSegment
#Arguments ProjectDirectory VideoName SouceLanguage DestinationLanguage AccentLanguage VoiceChannelLeft=0 VoiceChannelRight=1
#Language uses code ex: en, ua, fr, de etc.
def main():
    script_directory = os.path.dirname(__file__)
    os.chdir(script_directory)
    if len(sys.argv) < 6:
        print("Missing arguments")
    else:
        #abstraction layer to free vram for each subroutine (some objects like Spleeter stay in vram even after exiting scope or autodisposal)
        video_path = sys.argv[1]+'/'+sys.argv[2]
        proj = video_path.split('.mp4')[0]
        vocals = proj+'/audio.wav'
        os.mkdir(proj)
        audio = AudioSegment.from_file(video_path)
        audio.export(vocals, format='wav')

        arg = video_path.split('.mp4')[0]+'/vocals.wav'
        vocals = proj+'/vocals'
        arg2 = proj+'/accompaniment.wav'
        subprocess.run(['python',script_directory+f"/Diarize.py",vocals])
        #subprocess.run(['python',script_directory+f"/Transcribe.py", vocals, arg, sys.argv[3]])
        #subprocess.run(['python',script_directory+f"/Translate.py", vocals, script_directory, sys.argv[3], sys.argv[4]])        
        #subprocess.run(['python',script_directory+f"/synthesize.py", vocals, sys.argv[5], arg2])
        #subprocess.run(['python',script_directory+f"/RecoverVideo.py", video_path, vocals, sys.argv[1]])
        #shutil.rmtree(vocals)
        
if __name__ == "__main__":
    main()