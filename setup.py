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
        'numpy'
       ,'num2words'
       ,'openai-whisper'
       ,'spleeter'
       ,'audiostretchy'
       ,'pydub'
       ,'pyannote.audio'
       ,'transformers'
       ,'numba'
       ,'deep-translator'
       ,'ffmpeg-python'
       ,'language-tool-python'
       ,'ffmpeg-python'
       ,'yt_dlp'
    ],
    cmdclass={
        'custom_install': CustomInstallCommand,
    }
)
