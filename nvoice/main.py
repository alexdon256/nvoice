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
        vocals = sys.argv[1]+'/audio.wav'
        audio = AudioSegment.from_file(video_path)
        audio.export(vocals, format='wav')
        os.mkdir(proj)
        command = [
        "demucs",  # Assumes demucs is in your PATH.  If not, provide full path.
        "-n", "mdx_extra",  # Specify the model name
        "--two-stems", "vocals", # Only output vocals and other
        "-o", proj,  # Specify the output directory
        vocals,  # Path to the input audio file
        ]
        subprocess.run(command)
        arg = proj+'/mdx_extra/audio/vocals.wav'
        arg2 = proj+'/mdx_extra/audio/no_vocals.wav'
        subprocess.run(['python',script_directory+f"/Diarize.py",proj, arg])
        subprocess.run(['python',script_directory+f"/Transcribe.py", proj, arg, sys.argv[3]])
        subprocess.run(['python',script_directory+f"/Translate.py", proj, script_directory, sys.argv[3], sys.argv[4]])        
        subprocess.run(['python',script_directory+f"/synthesize.py", proj, sys.argv[5], arg2])
        subprocess.run(['python',script_directory+f"/RecoverVideo.py", video_path, proj, sys.argv[1]])
        
if __name__ == "__main__":
    main()