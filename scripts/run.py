"""
Main runner for the summariser.
"""

import argparse
import sys
import os

# Add the path to the lib directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.logger import logger
from lib.runner import summarise


def main():
    """
    Main entry point for the summariser.
    """
    parser = argparse.ArgumentParser(description="Process a file path or URL.")
    parser.add_argument("input-location", type=str, help="File path or URL to process.")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging.")
    parser.add_argument("--prompt", type=str, help="Prompt to use for GPT model")
    parser.add_argument("--model", type=str, default="gpt-3.5-turbo",
                         choices=["gpt-3.5-turbo", "gpt-4"],
                         help="OpenAI model to use for summarisation.")
    parser.add_argument("--force-content-type", type=str, choices=["youtube-url", "url", "audio-file", "text-file"],
                        help="Force the content type to be one of these options.")

    args = parser.parse_args()

    if args.debug:
        logger.level("DEBUG")

    summaries = summarise(args)

    for summary in summaries:
        print(f"{summary}")


if __name__ == "__main__":
    main()