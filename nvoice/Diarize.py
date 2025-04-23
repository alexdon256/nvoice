import os
import sys
import torch
import pickle
from pydub import AudioSegment
from speechbrain.pretrained import SpeakerDiarization
from pyannote.audio import Pipeline

class Diarizer:
    def __init__(self):
        self._diary = list()
        self._audio_path=''
        self.device = "cuda" 
        if not torch.cuda.is_available():
            self.device = "cpu"
        print(self.device)
        )
        self.pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1",
            use_auth_token="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", )
        
        self.pipeline.to(torch.device(self.device))
                
    def Diarize(self, audio_path):
        self._diary = list() 
        diary_folder = audio_path.split(".wav")[0]

            signal, sampling_rate = torchaudio.load(audio_path)

                print(f"Warning: Input audio has a sample rate of {sampling_rate} Hz, but the script expects {self.sampling_rate} Hz. This might affect diarization accuracy.")

            duration = signal.shape[1] / sampling_rate

            # Process the audio file for diarization
            with torch.no_grad():
                diarization = self.diarizer.diarize(audio_path)

            audio = AudioSegment.from_wav(audio_path)
            os.makedirs(diary_folder, exist_ok=True)

            speaker_segments = diarization.get_speaker_segments()

            for speaker, segments in speaker_segments.items():
                for segment in segments:
                    start_time = segment.start
                    end_time = segment.end
                    print(f"{start_time:.3f} {end_time:.3f} {speaker}")
                    self._diary.append([start_time, end_time, speaker])
                    # Extract audio segment
                    start_ms = int(start_time * 1000)
                    end_ms = int(end_time * 1000)
                    segment_audio = audio[start_ms:end_ms]
                    segment_filename = os.path.join(diary_folder, f"{speaker}_{start_time:.3f}-{end_time:.3f}.wav")
                    segment_audio.export(segment_filename, format="wav", parameters={"sample_rate": self.sampling_rate}) # Export at 44kHz

            with open(os.path.join(diary_folder, 'diary.pickle'), 'wb') as file:
                pickle.dump(self._diary, file, protocol=pickle.HIGHEST_PROTOCOL)

        except Exception as e:
            print(f"Error during diarization: {e}")

# outputs separate audio chunks of speech in wav format and pickle catalog into audio_path dir (first argument)
            end = turn.end
            print(start, end)
            self._diary.append([start, end, speaker])
            segment = audio[start:end]
            
        with open(diary_folder+'/diary.pickle', 'wb') as file:
            pickle.dump(self._diary, file, protocol=pickle.HIGHEST_PROTOCOL)

#outputs separate audio chunks of speach in wav format and csv catalog into audio_path dir (first argument)
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Missing argument audio_path")
    else:
        diarizer = Diarizer()
        diarizer.Diarize(sys.argv[1])
        