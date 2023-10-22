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
pip install git+https://github.com/chorsley/audio_summariser
```

## Usage

```markdown
`$ export OPENAI_API_KEY=<your key>`

`$ audio-summarise https://www.youtube.com/watch?v=3VEkzweBJPM`
# Summary of Transcript:
## Introduction
- The speaker claims to have received information that changed the course of their life six years ago.
- Allegations are made that the US government killed over 12 billion birds through the use of poisonous toxins dropped from airplanes over a period of 40 years.
- The purpose of killing the birds was to replace them with surveillance drone replicas disguised as birds.
- The speaker acknowledges that this may sound absurd but asks the audience to keep an open mind and be respectful.
...

`$ python scripts/run.py tests/Armstrong_Small_Step.ogg --prompt "What is this audio? How is it historically significant?"`
# Summary of the Audio Transcript: "I'm going to step off the LM now. That's one small step for a man, one giant leap for mankind."
## Historical Significance of the Audio

- The audio is a famous quote from astronaut Neil Armstrong during the Apollo 11 mission to the moon.
- It marks a significant moment in human history, as it was the first time a human being set foot on the moon.
- Neil Armstrong's words symbolize the achievement of the entire human race, emphasizing the monumental nature of the moment.
...

`$ audio-summarise mytranscript.txt`
...
```

Summarise can be used to summarise text files, audio files, and YouTube URLs. The summarisation process is the same for all three types of input, but the methods for processing the input are different.

```
$ export OPENAI_API_KEY=<your key>
$ audio-summarise --help
usage: audio-summarise [-h] [--debug] [--prompt PROMPT] [--model {gpt-3.5-turbo,gpt-4}]
              [--force-content-type {youtube-url,url,audio-file,text-file}]
              input-location

Process a file path or URL.

positional arguments:
  input-location        File path or URL to process.

options:
  -h, --help            show this help message and exit
  --debug               Enable debug logging.
  --prompt PROMPT       Prompt to use for GPT model
  --model {gpt-3.5-turbo,gpt-4}
                        OpenAI model to use for summarisation.
  --force-content-type {youtube-url,url,audio-file,text-file}
                        Force the content type to be one of these options.
```

# Contributing

If you'd like to contribute to Summarise, please fork the repository and create a pull request. We welcome contributions of all kinds, including bug fixes, new features, and documentation improvements.

## License

Summarise is licensed under the MIT License. See the LICENSE file for more information.
