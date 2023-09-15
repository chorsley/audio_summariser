from os import environ

import openai

from .tokenizer import Tokenizer

from .logger import logger

from .config import MAX_TOKENS
from .config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

# Initialize OpenAI API

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
            This is a continuation of a previous transcription chunk so factor that in too and assume we're continuing. That chunk ended like this:
            {prev_chunk.split(" ")[-100]}
            """


        logger.info(f"Summarising chunk {chunk_num} using prompt {prompt}...")

        if user_prompt:
            prompt += user_prompt

        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text}
            ],
            max_tokens=int(MAX_TOKENS[model] - Tokenizer.count(prompt) - Tokenizer.count(text)),
        )
        return response.choices[0]["message"]["content"].strip()