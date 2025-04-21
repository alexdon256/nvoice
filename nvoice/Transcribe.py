import sys
import torch
import pickle
from pydub import AudioSegment
import whisper
#from language_tool_python import LanguageTool

class Transcriber:
    def __init__(self, work_dir, audio_path, src_lang):
        
        self.wd = work_dir
        self.audio_path = audio_path
        self.src_lang = src_lang
        self.diary = []
        with open(work_dir+'/diary.pickle', 'rb') as file:
            self.diary = pickle.load(file)
        
        #Whisper pipeline
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
    #Here we are matching transcript data with speaker diarization
    #Some voice generation models are limited on the size of prompt
    #So TODO will be more elaborate way of sentense separation
    #i.e. break down diary record into chunks using timestamps from transcript where each chunk size>200 chars
    def _resolveDiary(self, time, text):
        for rec in self.diary:
            if time>rec[0] and time<rec[1]:
                return rec
            
    def _FitTranscript(self, chunks):
        transcription = []
        if len(chunks)>0:
            for rec in self.diary:
                rec.append('')
            
            #match speaker
            last_speaker = ''
            for chunk in chunks:
                
                avg_time = (chunk['seek'])
                speaker = next(filter(lambda x: x[0]<avg_time and x[1]>avg_time or x[0]>chunk['start'], self.diary), '')
                if speaker == '':
                    speaker=last_speaker
                if len(chunk['text'])>0 and speaker!='':
                    transcription.append([chunk['start'],chunk['end'],speaker[2],chunk['text']]) 
                last_speaer = speaker
        
            #remove empty text, correct grammar
            i=0
            #tool = LanguageTool(self.src_lang)
            while i < len(transcription)-1:
                text = transcription[i][3].strip()
                transcription[i][3] = text#tool.correct(text)
                
                i+=1
            i=0
            while i < len(transcription)-1:
                text = transcription[i][3].strip()
                if text.isspace():
                    transcription.pop(i)
                    i-=1
                i+=1            
            self.diary = transcription
            
    def Transcribe(self):
        model = whisper.load_model("turbo")
        transcript = model.transcribe(
            word_timestamps=True,
            audio=self.audio_path
        )
        self._FitTranscript(transcript['segments'])
        audio = AudioSegment.from_file(self.audio_path)
        
        for rec in self.diary:
            speaker = AudioSegment.silent(0,audio.frame_rate)
            speaker.export(self.wd+f'/{rec[2]}.wav', format='wav')
        i=0    
        for rec in self.diary:
            start = rec[0]
            end = rec[1]
            text = rec[3]
            speaker = rec[2]
            #rec[3] = GoogleTranslator(source=self.src_lang, target=self.dst_lang).translate(text)
            #save audio reference for every speaker
            referense_segment = audio[int(start*1000):int(end*1000)]
            speaker_path = self.wd+f'/{speaker}.wav'
            speaker_aud = AudioSegment.from_file(speaker_path)
            speaker_aud+=referense_segment
            speaker_aud.export(speaker_path, format="wav")
            referense_segment.export(self.wd+f'/{i}.wav', format="wav")
            
            rec.append(speaker_path)
            rec.append(self.wd+f'/{i}.wav')
            i+=1
            
        with open(self.wd+'/transcript.pickle', 'wb') as file:
            pickle.dump(self.diary, file, protocol=pickle.HIGHEST_PROTOCOL)
        
if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Missing argument audio_path")
    else:
        transcriber = Transcriber(sys.argv[1], sys.argv[2], sys.argv[3])
        transcriber.Transcribe()