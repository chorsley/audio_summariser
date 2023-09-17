from os import environ

import openai

from .tokenizer import Tokenizer

from .logger import logger

from .config import MAX_TOKENS
from .config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

PREV_CHUNK_TOKENS = 100


def gpt_summarise(model, prompt, text, max_tokens):
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text}
            ],
            max_tokens=max_tokens,
        )

        return response


class Summarizer:
    @staticmethod
    def summarize(text: str, user_prompt: str, model: str, chunk_num: int=0, prev_chunk: str="") -> str:
        prompt = """
          You are an audio transcription summariser bot.
          Break down the following text into a series of insightful bullet points summarising the main detail of this transcript.
          Format the output as markdown using headings and bullet points. Use h1 and h2 level headings and bullet points for details.
          Use numbered lists when the audio is listing a number of items.

          Also note that some text may be transcribed incorrectly; try to correct this where possible based on context.
        """

        if chunk_num != 0:
            prompt += f"""
            Between the "---" markers below is the last section of the previous transcription chunk.  Just use this to re-establish context.
            Don't repeat the points made in this previous chunk but factor them in to summarising the new text chunk. That previous chunk ended like this:
            ---
            {Tokenizer.get_last_n_string_tokens(prev_chunk, PREV_CHUNK_TOKENS, whole_words=True)}
            ---
            """


        logger.info(f"Summarising chunk {chunk_num} using prompt {prompt}...")

        if user_prompt:
            prompt += user_prompt

        response = gpt_summarise(model, prompt, text, MAX_TOKENS[model] - Tokenizer.count(prompt) - Tokenizer.count(text))
        logger.debug(f"RESPONSE: {response}")

        return response.choices[0]["message"]["content"].strip()