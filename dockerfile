FROM nvidia/cuda:12.1.0-base-ubuntu22.04
WORKDIR /
RUN apt-get update -y \
    && apt-get install -y python3-pip
RUN ldconfig /usr/local/cuda-12.1/compat/
RUN apt-get install zlib1g \
    && apt-get -y install cudnn9-cuda-12
RUN apt install git -y
RUN apt install ffmpeg -y
RUN pip install --no-cache-dir runpod
RUN pip install --no-cache-dir --upgrade wheel
RUN pip install --no-cache-dir ffmpeg-python
RUN pip install --no-cache-dir yt_dlp
RUN pip install --ignore-installed --no-deps git+https://github.com/chimneycrane/TTS.git;
RUN pip install --no-cache-dir librosa
RUN pip install --no-cache-dir anyascii
RUN pip install --no-cache-dir bangla
RUN pip install --no-cache-dir bnnumerizer
RUN pip install --no-cache-dir bnunicodenormalizer
RUN pip install --no-cache-dir coqpit
RUN pip install --no-cache-dir cython
RUN pip install --no-cache-dir encodec
RUN pip install --no-cache-dir flask
RUN pip install --no-cache-dir g2pkk
RUN pip install --no-cache-dir gruut[de,es,fr]
RUN pip install --no-cache-dir hangul_romanize
RUN pip install --no-cache-dir inflect
RUN pip install --no-cache-dir jamo
RUN pip install --no-cache-dir jieba
RUN pip install --no-cache-dir mutagen
RUN pip install --no-cache-dir nltk
RUN pip install --no-cache-dir pypinyin
RUN pip install --no-cache-dir pysbd
RUN pip install --no-cache-dir "spacy[ja]" #spacy[ja]
RUN pip install --no-cache-dir trainer
RUN pip install --no-cache-dir transformers
RUN pip install --no-cache-dir umap-learn
RUN pip install --no-cache-dir unidecode
RUN pip install --no-cache-dir flask
RUN pip install --no-cache-dir --ignore-installed num2words
RUN pip install --no-cache-dir --ignore-installed pydub
RUN pip install --no-cache-dir --ignore-installed audiostretchy
RUN pip install --no-cache-dir --ignore-installed deep-translator
RUN pip install --no-cache-dir --ignore-installed language-tool-python
RUN pip install --no-cache-dir inaSpeechSegmenter
RUN pip install --no-cache-dir demucs
RUN pip install --no-cache-dir pyannote.audio
RUN pip install --no-cache-dir stable-ts
RUN pip uninstall -y triton
RUN pip install --no-cache-dir triton==2.0.0
RUN apt install openjdk-17-jre -y
RUN apt install openjdk-17-jdk -y
RUN pip install --no-cache-dir langdetect
RUN pip install --no-cache-dir tensorflow==2.19.0
RUN pip install --no-cache-dir --force-reinstall numpy==1.25.0
RUN pip install --no-cache-dir pybind11==2.12
RUN pip uninstall torch torchaudio torchvision -y
RUN pip cache purge
RUN pip install --no-cache-dir torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cu121
RUN git clone https://github.com/alexdon256/nvoice.git
RUN pip install --no-cache-dir -e ./nvoice
CMD ["python3", "/nvoice/handler.py"]