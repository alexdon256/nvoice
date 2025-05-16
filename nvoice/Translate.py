import sys
import pickle
#from language_tool_python import LanguageTool
#from deep_translator import GoogleTranslator
import deepl
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

diary =[]
with open(sys.argv[1]+'/transcript.pickle', 'rb') as file:
    diary = pickle.load(file)
grammar_modifier = dict()
genders = dict()
for rec in diary:
    grammar_modifier[rec[2]] = rec[4]
try:
    for rec in grammar_modifier.keys():
        gender = 'male'
        seg = Segmenter()
        segment_length_ms = 30000  # 30 seconds
        audio = AudioSegment.from_file(grammar_modifier[rec])
        chunk = audio[0:30000]
        chunk.export(f"temp_chunk.wav", format="wav")
        segments = seg('./temp_chunk.wav') # Replace "audio.wav" with your audio file
        genders[rec] = 'male'
        for segment in segments:
            if segment[0] == 'male' or segment[0] == 'female':
                genders[rec] = segment[0]
                break
except FileNotFoundError as e:
    print(f"Error: Audio file not found for speaker {rec}: {e}")
    genders[rec] = None  # Or some other default value
except Exception as e:
    print(f"An unexpected error occurred while processing audio for speaker {rec}: {e}")
    genders[rec] = None  # Or some other default value
textblock = ''
translation = ''
i=0
translator = deepl.Translator('bc56d147-0ada-4789-806d-35359c319fc2:fx')
for rec in diary:
    feature = genders[rec[2]]
    rec[3] = replace_numbers_with_words(rec[3])
    textblock = textblock + f' ({feature}):| '+ rec[3] + ' ~ '
    if len(textblock) > 3000:
        translation = translation + translator.translate_text(
                                            textblock,
                                            target_lang=sys.argv[4]).text
                                        #GoogleTranslator(source=sys.argv[3], target=sys.argv[4]).translate(textblock)
        textblock = ''
    
if len(textblock) >  0:
        translation = translation + translator.translate_text(
                                            textblock,
                                            target_lang=sys.argv[4]).text#GoogleTranslator(source=sys.argv[3], target=sys.argv[4]).translate(textblock)

i=0
print(translation)
for block in translation.split('~'):
    if len(block)>0:
        print('i = ',i,block+'\n')
        if len(block.split('|'))>1:
            diary[i][3]=block.split('|')[1]
        else:
            diary[i][3]=block
    i+=1
with open(sys.argv[1]+'/transcript.pickle', 'wb') as file:
    pickle.dump(diary, file, protocol=pickle.HIGHEST_PROTOCOL)