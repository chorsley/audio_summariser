""" 
Main runner for the summariser separate from the CLI.
"""
import pprint
import argparse
from typing import List
from enum import Enum
from urllib.parse import urlparse
import mimetypes

from .logger import logger

from .tokenizer import Tokenizer
from .llm_summariser import Summarizer
from .audio_handler import AudioHandler


class ContentType(Enum):
    """
    Different types of content we can handle
    """
    YOUTUBE_URL = "youtube-url"
    URL = "url"
    AUDIO_FILE = "audio-file"
    TEXT_FILE = "text-file"


def detect_content_type(input_path: str) -> ContentType:
    """
    Detect the content type of the input.
    """
    # see if it's a URL or YouTube URL
    if input_path.startswith("http"):
        parsed_url = urlparse(input_path)

        if parsed_url.netloc.endswith("youtube.com"):
            return ContentType.YOUTUBE_URL
        elif parsed_url.scheme in ["http", "https"]:
            return ContentType.URL

    # fallback to file checking
    file_type, _ = mimetypes.guess_type(input_path)

    if file_type is None:
        raise ValueError(f"Could not detect content type of input. Check it exists: {input_path}")
    elif file_type.startswith("audio/"):
        return ContentType.AUDIO_FILE
    elif file_type.startswith("text/"):
        return ContentType.TEXT_FILE
    elif file_type.startswith("video/"):
        return ContentType.URL
    else:
        raise ValueError(f"Could not detect content type of input: {input_path}")


def summarise(args: argparse.Namespace):
    """
    Handle args and run summariser.
    """
    text_filename:str = ""
    summaries:List[str] = []
    input_location = getattr(args, "input-location")
    
    print(args)
    if args.force_content_type:
        try:
            content_type = ContentType(args.force_content_type)
        except KeyError:
            raise ValueError(f"Unsupported content type: {args.force_content_type}")
    else:
        content_type = detect_content_type(input_location)

    if content_type == ContentType.YOUTUBE_URL:
        audio_filename = AudioHandler.download_from_yt(input_location)
        audio_chunk_filenames = AudioHandler.split_into_chunks(audio_filename)
        logger.debug(f"Created audio file chunks from YouTube URL: {audio_chunk_filenames}")
        text_filename = AudioHandler.create_transcript(audio_chunk_filenames)
    elif content_type == ContentType.AUDIO_FILE:
        audio_chunk_filenames = AudioHandler.split_into_chunks(input_location)
        logger.debug(f"Created audio file from file: {audio_chunk_filenames}")
        text_filename = AudioHandler.create_transcript(audio_chunk_filenames)
    elif content_type == ContentType.TEXT_FILE:
        text_filename = input_location
    else:
        raise ValueError(f"Unsupported content type: {content_type}")

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
