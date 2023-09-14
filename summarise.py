import argparse
import sys
from os import environ
import tempfile

import openai
import tiktoken
import youtube_dl
from loguru import logger
from pydub import AudioSegment, silence


# Initialize OpenAI API
openai.api_key = environ["OPENAI_API_KEY"]

# Global max tokens
MAX_TOKENS = 8000

class YTLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def count_tokens(text: str) -> int:
    """
    Count tokens in a text using tiktoken.
    """
    encoding = tiktoken.encoding_for_model("gpt-4")
    num_tokens = len(encoding.encode(text))
    return num_tokens

def chunk_text(text: str) -> list[str]:
    """
    Breaks the text into chunks that fit into the GPT-4 token limit.
    """
    chunks = []
    current_chunk = ""
    for paragraph in text.split(". "):
        if count_tokens(current_chunk + paragraph) < MAX_TOKENS / 2:
            current_chunk += paragraph + ". "
        else:
            chunks.append(current_chunk)
            current_chunk = paragraph + ". "
    if current_chunk:
        chunks.append(current_chunk)
    for chunk in chunks:
        print(count_tokens(chunk))
    return chunks

def summarize_text(text: str, user_prompt: str) -> str:
    """
    Summarize a chunk of text using GPT-4.
    """
    prompt = f"""
      You are an audio transcription summariser bot.
      Break down the following text into a series of insightful bullet points summarising the main detail of this transcript.
      Format the output as markdown using headings and bullet points. Also note that some text may be transcribed incorrectly;
      try to correct this where possible based on context.
    """

    if user_prompt:
        prompt = prompt + user_prompt

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": prompt}, 
            {"role": "user", "content": text}
        ],
        max_tokens=int(MAX_TOKENS / 2)  # Using the global MAX_TOKENS
    )
    # print(response)
    return response.choices[0]["message"]["content"].strip()

def create_transcript_from_audio_file(audio_chunk_filenames: list[str]) -> str:
    """
    Return the filename of a Whisper transcript file created from a list of audio files.
    """

    transcript_filename = tempfile.NamedTemporaryFile().name + ".txt"

    # write the transcript to a file
    with open(transcript_filename, "w") as file:
        # use openai's whisper API to make a transcript
        for filepath in audio_chunk_filenames:
            audio_file= open(filepath, "rb")
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
            file.write(transcript.get("text"))

    return transcript_filename

def create_audio_file_from_yt_url(url: str) -> str:
    """
    Download audio from a YouTube video.
    """
    # create a unique temp file name

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


def split_audio_file_into_chunks(filepath: str) -> list[str]:
    """
    Split an audio file into chunks.
    """

    chunk_paths = []

    sound1 = AudioSegment.from_file(filepath)
    step_size = 60*1000*5
    #chunks = silence.split_on_silence(sound1, min_silence_len=1000, seek_step=step_size, silence_thresh=-40)
    # split into 15 minute chunks - not so nice that audio is cut off mid-sentence.
    # split_on_silence needs more control over maximum chunk size.
    chunks = sound1[::1000 * 60 * 15]

    #for i, chunk in enumerate([sound1[:step_size]] + chunks):
    for i, chunk in enumerate(chunks):
        audio_file_name = f"{tempfile.NamedTemporaryFile().name}_{i}.mp3"
        with open(audio_file_name, "wb") as f:
            chunk.export(f, format="mp3")
        chunk_paths.append(audio_file_name)

    return chunk_paths

def main():
    parser = argparse.ArgumentParser(description="Process a file path or YouTube URL.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--transcript_file", type=str, help="Transcript file to process.")
    group.add_argument("--audio_file", type=str, help="Audio file to process.")
    group.add_argument("--url", type=str, help="YouTube URL to process.")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging.")
    parser.add_argument("--prompt", type=str, help="Prompt to use for GPT-4.")

    args = parser.parse_args()

    if args.debug:
        logger.level("DEBUG")

    text_filename:str = None

    if args.url:
        audio_filename = create_audio_file_from_yt_url(args.url)
        audio_chunk_filenames = split_audio_file_into_chunks(audio_filename)
        logger.debug(f"Created audio file chunks from YouTube URL: {audio_chunk_filenames}")
        text_filename = create_transcript_from_audio_file(audio_chunk_filenames)
    elif args.audio_file:
        audio_chunk_filenames = split_audio_file_into_chunks(args.audio_file)
        logger.debug(f"Created audio file from file: {audio_chunk_filenames}")
        text_filename = create_transcript_from_audio_file(audio_chunk_filenames)
    else:
        text_filename = args.transcript_file
    logger.debug(f"Processing {text_filename}")

    with open(text_filename, 'r') as f:
        text = f.read()

    logger.debug(f"Text: {text}")

    chunks = chunk_text(text)
    logger.info(f"Summarising {len(chunks)} chunk(s)...")
    summaries = [summarize_text(chunk, args.prompt) for chunk in chunks]

    print("Summary:")
    for idx, summary in enumerate(summaries, 1):
        print(f"{summary}")

if __name__ == "__main__":
    main()

