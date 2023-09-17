import sys
import os
import argparse
import unittest
from unittest.mock import patch, MagicMock

# Add the path to the lib directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.runner import summarise
# Import the modules to be mocked
from lib.llm_summariser import Summarizer
from lib.audio_handler import AudioHandler
from lib.tokenizer import Tokenizer

class Dict2Class(object):
      
    def __init__(self, my_dict):
          
        for key in my_dict:
            setattr(self, key, my_dict[key])


basic_openai_completion_mock_response = {
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


class TestGetStringTokens(unittest.TestCase):
    def test_summarise_input_transcript(self):
        with patch("lib.llm_summariser.gpt_summarise", return_value=Dict2Class(basic_openai_completion_mock_response)):
            args = argparse.Namespace(
                input_transcript="tests/test.txt",
                debug=False,
                prompt=None,
                model="gpt-3.5-turbo",
                input_audio_file=None,
                input_youtube_url=None
            )
            summaries = summarise(args)
            print(summaries)
            assert len(summaries) == 1
            assert summaries[0] == "This is a test transcript."

    def test_summarise_input_audio_file(self):
        with patch("lib.llm_summariser.gpt_summarise", return_value=Dict2Class(basic_openai_completion_mock_response)):
            args = argparse.Namespace(
                input_transcript=None,
                debug=False,
                prompt=None,
                model="gpt-3.5-turbo",
                input_audio_file="tests/Armstrong_Small_Step.ogg",
                input_youtube_url=None
            )
            summaries = summarise(args)
            print(summaries)
            assert len(summaries) == 1
            assert summaries[0] == "This is a test transcript."