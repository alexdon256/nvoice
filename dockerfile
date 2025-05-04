FROM nvidia/cuda:12.1.0-base-ubuntu22.04
RUN apt-get update -y \
    && apt-get install -y python3-pip
RUN ldconfig /usr/local/cuda-12.1/compat/
RUN apt-get install zlib1g \
    && apt-get -y install cudnn9-cuda-12
RUN apt install ffmpeg -y
RUN pip install --no-cache-dir runpod
RUN pip install --upgrade wheel
RUN pip install ffmpeg-python
RUN pip install yt_dlp
RUN pip install --ignore-installed --no-deps git+https://github.com/chimneycrane/TTS.git;
RUN pip install librosa
RUN pip install anyascii
RUN pip install bangla
RUN pip install bnnumerizer
RUN pip install bnunicodenormalizer
RUN pip install coqpit
RUN pip install cython
RUN pip install encodec
RUN pip install flask
RUN pip install g2pkk
RUN pip install gruut[de,es,fr]
RUN pip install hangul_romanize
RUN pip install inflect
RUN pip install jamo
RUN pip install jieba
RUN pip install mutagen
RUN pip install nltk
RUN pip install pypinyin
RUN pip install pysbd
RUN pip install "spacy[ja]" #spacy[ja]
RUN pip install trainer
RUN pip install transformers
RUN pip install umap-learn
RUN pip install unidecode
RUN pip install flask
RUN pip install --ignore-installed num2words
RUN pip install --ignore-installed pydub
RUN pip install --ignore-installed audiostretchy
RUN pip install --ignore-installed deep-translator
RUN pip install --ignore-installed language-tool-python
RUN pip install inaSpeechSegmenter
RUN pip install demucs
RUN pip install pyannote.audio
RUN pip install stable-ts
RUN pip uninstall -y triton
RUN pip install triton==2.0.0
RUN apt install openjdk-17-jre -y
RUN apt install openjdk-17-jdk -y
RUN pip install langdetect
RUN pip install tensorflow==2.19.0
RUN pip install --force-reinstall numpy==1.25.0
RUN pip install pybind11==2.12
RUN pip uninstall torch torchaudio torchvision -y
RUN pip cache purge
RUN pip install torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cu121
RUN git clone https://github.com/alexdon256/nvoice.git
RUN pip install -e ./nvoice
CMD ["python3", "/nvoice/handler.py"]