import os
import sys
import torch
import pickle
from pydub import AudioSegment
from speechbrain.pretrained import DiarizationBrain
import torchaudio

class Diarizer:
    def __init__(self):
        self._diary = list()
        self._audio_path = ''
        self.device = "cuda"
        if not torch.cuda.is_available():
            self.device = "cpu"
        print(self.device)
        self.diarizer = DiarizationBrain.from_hparams(
            source="speechbrain/diarization-xvector-voxceleb",
            savedir="pretrained_models/diarization-xvector-voxceleb",
        )
        self.sampling_rate = 44000  # Expected sample rate of input files

    def Diarize(self, audio_path):
        self._diary = list()
        self._audio_path = audio_path
        diary_folder = audio_path.split(".wav")[0]

        try:
            signal, sampling_rate = torchaudio.load(audio_path)

            # Check if the loaded sample rate matches the expected rate
            if sampling_rate != self.sampling_rate:
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
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Missing argument audio_path")
    else:
        diarizer = Diarizer()
        diarizer.Diarize(sys.argv[1])