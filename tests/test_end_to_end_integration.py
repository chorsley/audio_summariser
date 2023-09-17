import sys
import os
import argparse
import unittest
from unittest.mock import patch

# Add the path to the lib directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.runner import summarise
# Import the modules to be mocked
from lib.llm_summariser import Summarizer
from lib.audio_handler import AudioHandler
from lib.tokenizer import Tokenizer

class Dict2Class(object):
    """
    Convert a dictionary to a class.

    Lets us mock the OpenAI response based on API JSON.
    """

    def __init__(self, my_dict):

        for key in my_dict:
            setattr(self, key, my_dict[key])


basic_openai_gpt_completion_mock_response = {
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "message": {
        "content": "This is a test transcript.",
        "role": "assistant"
      }
    }
  ],
  "created": 1677664795,
  "id": "chatcmpl-7QyqpwdfhqwajicIEznoc6Q47XAyW",
  "model": "gpt-3.5-turbo-0613",
  "object": "chat.completion",
  "usage": {
    "completion_tokens": 17,
    "prompt_tokens": 57,
    "total_tokens": 74
  }
}

basic_openai_whisper_completion_mock_response = {
  "text": "This is a test transcript."
}


class TestGetStringTokens(unittest.TestCase):


    def test_summarise_input_transcript(self):
        with patch("lib.llm_summariser.gpt_summarise", return_value=Dict2Class(basic_openai_gpt_completion_mock_response)):
            args = argparse.Namespace(
                input_transcript="tests/test.txt",
                debug=False,
                prompt=None,
                model="gpt-3.5-turbo",
                input_audio_file=None,
                input_youtube_url=None
            )
            summaries = summarise(args)
            assert len(summaries) == 1
            assert summaries[0] == "This is a test transcript."

    def test_summarise_input_audio_file(self):
        with patch("lib.audio_handler.get_openai_whisper_transcript", return_value=basic_openai_whisper_completion_mock_response):
             with patch("lib.llm_summariser.gpt_summarise", return_value=Dict2Class(basic_openai_gpt_completion_mock_response)):
                args = argparse.Namespace(
                    input_transcript=None,
                    debug=False,
                    prompt=None,
                    model="gpt-3.5-turbo",
                    input_audio_file="tests/Neil_Armstrong_small_step.wav",
                    input_youtube_url=None
                )
                summaries = summarise(args)
                assert len(summaries) == 1
                assert summaries[0] == "This is a test transcript."

    def test_summarise_input_youtube_url(self):
        """
        This test is a bit more complicated because it requires mocking the YouTube downloader.
        """
        with patch("lib.audio_handler.youtube_dl_to_file") as mock_youtube_dl_to_file:
            mock_youtube_dl_to_file.return_value = "tests/Neil_Armstrong_small_step.wav"
            with patch("lib.audio_handler.get_openai_whisper_transcript", return_value=basic_openai_whisper_completion_mock_response):
                with patch("lib.llm_summariser.gpt_summarise", return_value=Dict2Class(basic_openai_gpt_completion_mock_response)):
                    args = argparse.Namespace(
                        input_transcript=None,
                        debug=False,
                        prompt=None,
                        model="gpt-3.5-turbo",
                        input_audio_file=None,
                        input_youtube_url="https://www.youtube.com/watch?v=2JlVqfC8-UI"
                    )
                    summaries = summarise(args)
                    assert len(summaries) == 1
                    assert summaries[0] == "This is a test transcript."