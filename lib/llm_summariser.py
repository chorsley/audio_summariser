from os import environ

import openai

from .config import MAX_TOKENS

# Initialize OpenAI API
openai.api_key = environ["OPENAI_API_KEY"]

class Summarizer:
    @staticmethod
    def summarize(text: str, user_prompt: str) -> str:
        prompt = """
          You are an audio transcription summariser bot.
          Break down the following text into a series of insightful bullet points summarising the main detail of this transcript.
          Format the output as markdown using headings and bullet points. Also note that some text may be transcribed incorrectly;
          try to correct this where possible based on context.
        """
        if user_prompt:
            prompt += user_prompt

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text}
            ],
            max_tokens=int(MAX_TOKENS / 2)
        )
        return response.choices[0]["message"]["content"].strip()