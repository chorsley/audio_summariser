import argparse
import sys
from os import environ
import tempfile

from loguru import logger

from lib.tokenizer import Tokenizer
from lib.llm_summariser import Summarizer
from lib.audio_handler import AudioHandler


def summarise(args):
    text_filename = None

    if args.url:
        audio_filename = AudioHandler.download_from_yt(args.url)
        audio_chunk_filenames = AudioHandler.split_into_chunks(audio_filename)
        logger.debug(f"Created audio file chunks from YouTube URL: {audio_chunk_filenames}")
        text_filename = AudioHandler.create_transcript(audio_chunk_filenames)
    elif args.audio_file:
        audio_chunk_filenames = AudioHandler.split_into_chunks(args.audio_file)
        logger.debug(f"Created audio file from file: {audio_chunk_filenames}")
        text_filename = AudioHandler.create_transcript(audio_chunk_filenames)
    else:
        text_filename = args.transcript_file
    logger.debug(f"Processing {text_filename}")

    with open(text_filename, 'r') as f:
        text = f.read()

    logger.debug(f"Text: {text}")
    chunks = Tokenizer.chunk(text)
    logger.info(f"Summarising {len(chunks)} chunk(s)...")
    summaries = [Summarizer.summarize(chunk, args.prompt) for chunk in chunks]

    return summaries


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

    summaries = summarise(args)

    print("Summary:")
    for idx, summary in enumerate(summaries, 1):
        print(f"{summary}")


if __name__ == "__main__":
    main()