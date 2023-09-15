import argparse
import sys
from os import environ
import tempfile


from lib.logger import logger
from lib.tokenizer import Tokenizer
from lib.llm_summariser import Summarizer
from lib.audio_handler import AudioHandler


def summarise(args):
    text_filename = None
    summaries = []

    if args.yt_url:
        audio_filename = AudioHandler.download_from_yt(args.yt_url)
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
    chunks = Tokenizer.chunk(text, model=args.model)
    logger.info(f"Summarising {len(chunks)} chunk(s)...")

    import pprint
    logger.debug(f"Chunks: {pprint.pformat(chunks)}")

    for chunk_num, chunk in enumerate(chunks):
        prev_chunk = summaries[chunk_num - 1] if chunk_num > 0 else ""

        summaries.append(Summarizer.summarize(chunk, args.prompt, model=args.model, chunk_num=chunk_num, prev_chunk=prev_chunk))


    return summaries


def main():
    parser = argparse.ArgumentParser(description="Process a file path or YouTube URL.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--transcript_file", type=str, help="Transcript file to process.")
    group.add_argument("--audio_file", type=str, help="Audio file to process.")
    group.add_argument("--yt_url", type=str, help="YouTube URL to process.")
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