import sys
import pickle
#from language_tool_python import LanguageTool
from deep_translator import GoogleTranslator
from pydub import AudioSegment
from langdetect import detect
from num2words import num2words
from inaSpeechSegmenter import Segmenter

def replace_numbers_with_words(text):
    words = text.split()
    new_words = []
    for word in words:
        if word.isdigit():
            new_words.append(num2words(int(word), lang=sys.argv[3]))
        else:
            new_words.append(word)
    return " ".join(new_words)
print('Translating')
diary =[]
with open(sys.argv[1]+'/transcript.pickle', 'rb') as file:
    diary = pickle.load(file)
grammar_modifier = dict()
genders = dict()
for rec in diary:
    print('0SEGMENT: ')
    grammar_modifier[rec[2]] = rec[4]
for rec in grammar_modifier.keys():
    print('1SEGMENT: ')
    gender = 'male'
    seg = Segmenter()
    segment_length_ms = 30000  # 30 seconds
    audio = AudioSegment.from_file(grammar_modifier[rec])
    chunk = audio[0:30000]
    chunk.export(f"temp_chunk.wav", format="wav")
    segments = seg('./temp_chunk.wav') # Replace "audio.wav" with your audio file
    for segment in segments:
        if segment[0] == 'male' or segment[0] == 'female':  
            print(rec+' SEGMENT: '+segment[0])
            genders[rec] = segment[0]
            break
        
for rec in diary:
    language = detect(rec[3])
    if language != sys.argv[4]:
        speaker_aud = AudioSegment.from_file(rec[4])
        feature = genders[rec[2]]
        rec[3] = replace_numbers_with_words(rec[3])
        
        translation = GoogleTranslator(source=sys.argv[3], target=sys.argv[4]).translate(f'({feature}):| '+rec[3])#
        rec[3] = translation.split('|')[1]
        print(rec[3])
        rec.append(1)
    else:
        rec.append(0)
    print(rec)
with open(sys.argv[1]+'/transcript.pickle', 'wb') as file:
    pickle.dump(diary, file, protocol=pickle.HIGHEST_PROTOCOL)