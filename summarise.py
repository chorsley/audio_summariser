import argparse
import sys
from os import environ
import tempfile


from lib.logger import logger
from lib.tokenizer import Tokenizer
from lib.llm_summariser import Summarizer
from lib.audio_handler import AudioHandler
from lib.runner import summarise


def main():
    parser = argparse.ArgumentParser(description="Process a file path or YouTube URL.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--input-transcript", type=str, help="Transcript file to process.")
    group.add_argument("--input-audio-file", type=str, help="Audio file to process.")
    group.add_argument("--input-youtube-url", type=str, help="YouTube URL to process.")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging.")
    parser.add_argument("--prompt", type=str, help="Prompt to use for GPT model")
    parser.add_argument("--model", type=str, default="gpt-3.5-turbo", choices=["gpt-3.5-turbo", "gpt-4"], help="OpenAI model to use for summarisation.")

    args = parser.parse_args()

    if args.debug:
        logger.level("DEBUG")

    summaries = summarise(args)

    print("Summary:")
    for idx, summary in enumerate(summaries, 1):
        print(f"{summary}")


if __name__ == "__main__":
    main()