""" 
Main runner for the summariser separate from the CLI.
"""
import pprint
import argparse
from typing import List

from .logger import logger

from .tokenizer import Tokenizer
from .llm_summariser import Summarizer
from .audio_handler import AudioHandler

def summarise(args: argparse.Namespace):
    """
    Handle args and run summariser.
    """
    text_filename:str = ""
    summaries:List[str] = []

    if args.input_youtube_url:
        audio_filename = AudioHandler.download_from_yt(args.input_youtube_url)
        audio_chunk_filenames = AudioHandler.split_into_chunks(audio_filename)
        logger.debug(f"Created audio file chunks from YouTube URL: {audio_chunk_filenames}")
        text_filename = AudioHandler.create_transcript(audio_chunk_filenames)
    elif args.input_audio_file:
        audio_chunk_filenames = AudioHandler.split_into_chunks(args.input_audio_file)
        logger.debug(f"Created audio file from file: {audio_chunk_filenames}")
        text_filename = AudioHandler.create_transcript(audio_chunk_filenames)
    else:
        text_filename = args.input_transcript
    logger.debug(f"Processing {text_filename}")

    with open(text_filename, 'r', encoding="utf-8") as f_text_filename:
        text = f_text_filename.read()

    logger.debug(f"Text: {text}")
    chunks = Tokenizer.chunk(text, model=args.model)
    logger.info(f"Summarising {len(chunks)} chunk(s)...")

    logger.debug(f"Chunks: {pprint.pformat(chunks)}")

    for chunk_num, chunk in enumerate(chunks):
        prev_chunk = summaries[chunk_num - 1] if chunk_num > 0 else ""

        summaries.append(
            Summarizer.summarize(chunk, args.prompt, model=args.model,
                                chunk_num=chunk_num, prev_chunk=prev_chunk)
        )


    return summaries
