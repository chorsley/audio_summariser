import tempfile
from os import environ

import youtube_dl
import openai
from pydub import AudioSegment, silence

from .logger import logger

# Initialize OpenAI API
from .config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

class YTLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def youtube_dl_to_file(url: str) -> str:
    audio_file_name = tempfile.NamedTemporaryFile().name + ".mp3"
    ydl_opts = {
    'keepvideo': True,
    'format': 'bestaudio/best',
    'outtmpl': audio_file_name,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '128'
    }],
    'logger': YTLogger()
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return audio_file_name


def get_openai_whisper_transcript(audio_filepath: str) -> dict:
    with open(audio_filepath, "rb") as audio_file:
        return openai.Audio.transcribe("whisper-1", audio_file)


class AudioHandler:
    @staticmethod
    def download_from_yt(url: str) -> str:
        audio_file_name = youtube_dl_to_file(url)
        return audio_file_name

    @staticmethod
    def split_into_chunks(filepath: str) -> list[str]:
        logger.debug(f"Splitting audio file {filepath} into chunks...")
        chunk_paths = []
        sound = AudioSegment.from_file(filepath)
        chunks = sound[::1000 * 60 * 15]
        for i, chunk in enumerate(chunks):
            audio_file_name = f"{tempfile.NamedTemporaryFile().name}_{i}.mp3"
            with open(audio_file_name, "wb") as f:
                chunk.export(f, format="mp3")
            chunk_paths.append(audio_file_name)
        return chunk_paths

    @staticmethod
    def create_transcript(audio_chunk_filenames: list) -> str:
        transcript_filename = tempfile.NamedTemporaryFile().name + ".txt"
        with open(transcript_filename, "w") as file:
            for filepath in audio_chunk_filenames:
                transcript = get_openai_whisper_transcript(filepath)
                file.write(str(transcript.get("text")))
        return transcript_filename