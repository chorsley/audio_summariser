import unittest
import re

import sys
import os

# Add the path to the lib directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Assuming tiktoken is a module you have access to.
from lib.tokenizer import Tokenizer

class TestGetStringTokens(unittest.TestCase):

    def test_get_last_token(self):
        text = "This is a test string."
        result = Tokenizer.get_last_n_string_tokens(text, 1, whole_words=False)
        self.assertEqual(result, ".")  # Last token is ".".

    def test_get_last_n_tokens_exact(self):
        text = "This is a test string."
        result = Tokenizer.get_last_n_string_tokens(text, 2, whole_words=False)
        # Assuming that tiktoken splits tokens as words and punctuation.
        self.assertEqual(result, " string.") 

    def test_get_last_n_tokens_whole_word(self):
        text = "This is a test string."
        result = Tokenizer.get_last_n_string_tokens(text, 2, whole_words=True)
        # Assuming tiktoken recognizes "string." as two separate tokens "string" and ".".
        # Thus, to get the last whole word, it should return just "string".
        self.assertEqual(result, " string.")

    def test_get_last_n_tokens_whole_word_end_in_unfamiliar_word_round_down(self):
        text = "This is a pwzdre string."
        result = Tokenizer.get_last_n_string_tokens(text, 4, whole_words=True)
        # pwzdre would be split up as multiple tokens, so it should return the last whole word "string" rounding backwards.
        self.assertEqual(result, " string.")

    def test_get_last_n_tokens_whole_word_unfamiliar_word_cover_character_tokens(self):
        text = "This is a pwzdre string."
        result = Tokenizer.get_last_n_string_tokens(text, 5, whole_words=True)
        # pwzdre would be split up as multiple tokens, so if we increase the token count we should get the whole unfamiliar word.
        self.assertEqual(result, " pwzdre string.")

    def test_get_last_n_tokens_factor_heading(self):
        text = "# heading\n\nThis is a pwzdre string."
        result = Tokenizer.get_last_n_string_tokens(text, 11, whole_words=True)
        # pwzdre would be split up as multiple tokens, so if we increase the token count we should get the whole unfamiliar word.
        self.assertEqual(result, "# heading\n\nThis is a pwzdre string.")

    def test_get_last_n_tokens_factor_heading_cut_heading_marker(self):
        text = "# heading\n\nThis is a pwzdre string."
        result = Tokenizer.get_last_n_string_tokens(text, 10, whole_words=True)
        # test falling short of the heading marker.
        self.assertEqual(result, " heading\n\nThis is a pwzdre string.")

    def test_get_last_n_tokens_greater_than_token_length(self):
        text = "# heading\n\nThis is a pwzdre string."
        result = Tokenizer.get_last_n_string_tokens(text, 1000, whole_words=True)
        # just return all text if token count is greater than the length of the text.
        self.assertEqual(result, "# heading\n\nThis is a pwzdre string.")

    def test_get_last_n_tokens_with_no_text(self):
        text = ""
        result = Tokenizer.get_last_n_string_tokens(text, 2, whole_words=True)
        self.assertEqual(result, "")

    # Additional tests can be added to handle various edge cases.

if __name__ == "__main__":
    unittest.main()