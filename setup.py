from setuptools import setup, Command, find_packages

class CustomInstallCommand(Command):
    def run(self):
        import subprocess
        subprocess.call(['pip', 'install', 'protobuf==3.20.0','--force-install'])
        
setup(
    name='nvoice',  # Replace with your desired package name
    python_requires='>=3.9',
    version='1.0.0',  # Replace with your desired version
    description='Video dubbing package',
    author='Alex Don',
    author_email='oleksandr.don.256@gmail.com',
    packages=find_packages(),
    setup_requires=['setuptools_git'],
    entry_points={
        'console_scripts': [
            'nvoice=main:main',
        ],
    },
    extras_require={
        'proto': ['protobuf==3.20.0'],  # Specific version for tts
    },
    install_requires=[
        'typer'
       ,'pandas'
       ,'scipy'
       ,'num2words'
       ,'audiostretchy'
       ,'numpy'
       ,'openai-whisper'
       ,'pytube'
       ,'pydub'
       ,'deep-translator'
       ,'ipython'
       ,'ffmpeg-python'
       ,'language-tool-python'
       ,'yt_dlp'
       ,'click==8.1.3'
       ,'spleeter==2.4.2'
       ,'torch==2.6.0'
       ,'typing-extensions==4.12.2'
       ,'typer==0.12.1'
       ,'httpx==0.25.0'
    ],
    cmdclass={
        'custom_install': CustomInstallCommand,
    }
)
