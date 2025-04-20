from setuptools import setup, Command, find_packages

class CustomInstallCommand(Command):
    def run(self):
        import subprocess
        subprocess.call(['pip', 'install', 'protobuf==3.20.0','--force-install'])
        
setup(
    name='nvoice',  # Replace with your desired package name
    python_requires='>=3.10',
    version='1.0.0',  # Replace with your desired version
    description='Video dubbing package',
    author='Alex Don',
    author_email='oleksandr.don.256@gmail.com',
    packages=find_packages(),
    setup_requires=['setuptools_git'],
    entry_points={
        'console_scripts': [
            'nvoice=nvoice.main:main',
        ],
    },
    extras_require={
        'proto': ['protobuf==3.20.0'],  # Specific version for tts
    },
    install_requires=[
        'numpy==1.22.0'
       ,'num2words'
       ,'openai-whisper==20231117'
       ,'spleeter==2.4.2'
       ,'audiostretchy'
       ,'httpx[http2]==0.19.0'
       ,'pydub==0.25.1'
       ,'pyannote.audio==3.1.1'
       ,'transformers'
       ,'numba'
       ,'deep-translator'
       ,'ipython==7.34.0'
       ,'ffmpeg-python'
       ,'language-tool-python'
       ,'ffmpeg-python'
       ,'yt_dlp'
    ],
    cmdclass={
        'custom_install': CustomInstallCommand,
    }
)
