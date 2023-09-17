# Summarise

Summarise produced LLM-powered summaries of text and audio files. Got a three hour training video and wondering if it's worth your time? Summarise it!

There are tools like this around for web browsers, but this is purely CLI-based for automate such things via the command line. 

It also supports summarising audio and text of any length (your OpenAI hard budget limits willing). It's BYO OpenAI key.

* from Youtube
* from an audio / video file locally
* from an already generated transcript file

## Installation

To install Summarise, you can use pip:

```bash
pip install https://github.com/chorsley/audio_summariser
```

## Usage

Summarise can be used to summarise text files, audio files, and YouTube URLs. The summarisation process is the same for all three types of input, but the methods for processing the input are different.

### Summarising text files

```
$ export OPENAI_API_KEY=<your key>
$ summarise --help
usage: summarise.py [-h]
                    (--input-transcript INPUT_TRANSCRIPT | --input-audio-file INPUT_AUDIO_FILE | --input-youtube-url INPUT_YOUTUBE_URL)
                    [--debug] [--prompt PROMPT] [--model {gpt-3.5-turbo,gpt-4}]

Process a file path or YouTube URL.

options:
  -h, --help            show this help message and exit
  --input-transcript INPUT_TRANSCRIPT
                        Transcript file to process.
  --input-audio-file INPUT_AUDIO_FILE
                        Audio file to process.
  --input-youtube-url INPUT_YOUTUBE_URL
                        YouTube URL to process.
  --debug               Enable debug logging.
  --prompt PROMPT       Custom, supplementary prompt to use for GPT model (e.g. "Make it understandable for a 5 year old.")
  --model {gpt-3.5-turbo,gpt-4}
                        OpenAI model to use for summarisation.
```

# Contributing

If you'd like to contribute to Summarise, please fork the repository and create a pull request. We welcome contributions of all kinds, including bug fixes, new features, and documentation improvements.

## License

Summarise is licensed under the MIT License. See the LICENSE file for more information.
