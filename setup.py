"""
Setup script for the audio_summariser package.
"""

import os
from setuptools import setup, find_packages

# Determine the path to this file (setup.py)
here = os.path.abspath(os.path.dirname(__file__))

# Use the path to derive the path to requirements.txt
req_file = os.path.join(here, 'requirements.txt')

# Read in the requirements.txt file
with open(req_file, "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="audio_summariser",
    version="0.1.0",
    packages=find_packages(),
    install_requires=requirements,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'audio-summarise=scripts.run:main',
        ],
    },
    author="Chris Horsley",
    author_email="github@falconmouse.com",
    description="Transcribe summarise audio transcripts using OpenAI services.",
    license="LICENSE.txt",
    keywords="youtube audio transcription summary whisper gpt openai",
    url="http://github.com/chorsley/audio_summariser",
)
