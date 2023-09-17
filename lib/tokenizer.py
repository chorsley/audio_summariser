"""
Used for counting and chunking text.
"""

import re

import tiktoken

from .config import MAX_TOKENS

class Tokenizer:
    """
    Class for tokenizing text and determining the number of tokens in a string.
    """
    @staticmethod
    def count(text: str) -> int:
        """
        Count the number of tokens in a string.
        """
        encoding = tiktoken.encoding_for_model("gpt-4")
        return len(encoding.encode(text))

    @staticmethod
    def get_last_n_string_tokens(text: str, token_count: int, whole_words=True) -> str:
        """
        Get the last n tokens from a string.
        Params:
            text: The text to get the last n tokens from.
            tokens: The number of tokens to get.
            whole_words: Whether to get whole words or not. You may get less then n tokens if this is set to true.
        """
        encoding = tiktoken.encoding_for_model("gpt-4")
        tokens = encoding.encode(text)[-token_count:]
        rounded_token_count = token_count

        decoded_tokens = encoding.decode(tokens[-rounded_token_count:])

        # If we want whole words, we need to get the last n tokens and then decode them to get the last n words.
        if whole_words:
            while token_count - rounded_token_count < 10:
                decoded_tokens = encoding.decode(tokens[-rounded_token_count:])
                if re.match(r"^[\s\-#]", decoded_tokens):
                    return decoded_tokens
                else:
                    rounded_token_count -= 1

        return decoded_tokens

    @staticmethod
    def chunk(text: str, model: str) -> list[str]:
        """
        Chunk text into smaller chunks of text based on model.
        """
        chunks = []
        current_chunk = ""
        for paragraph in text.split(". "):
            if Tokenizer.count(current_chunk + paragraph) < MAX_TOKENS[model] // 2:
                current_chunk += paragraph + ". "
            else:
                chunks.append(current_chunk)
                current_chunk = paragraph + ". "
        if current_chunk:
            chunks.append(current_chunk)
        for chunk in chunks:
            print(Tokenizer.count(chunk))
        return chunks