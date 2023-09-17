from setuptools import setup, find_packages

# Read in the requirements.txt file
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="Audio Summariser",
    version="0.1.0",
    packages=find_packages(),
    install_requires=requirements,
    package_data={
    },
    entry_points={
        'console_scripts': [
            'audio_summarise=summarise.py:main',
        ],
    },
    author="Chris Horsley",
    author_email="github@falconmouse.com",
    description="Transcribe summarise audio transcripts using OpenAI services.",
    license="LICENSE.txt",
    keywords="youtube audio transcription summary whisper gpt openai",
    url="http://github.com/chorsley/audio_summariser",
)