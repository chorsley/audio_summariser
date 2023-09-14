import tiktoken

from .config import MAX_TOKENS

class Tokenizer:
    @staticmethod
    def count(text: str) -> int:
        encoding = tiktoken.encoding_for_model("gpt-4")
        return len(encoding.encode(text))

    @staticmethod
    def chunk(text: str) -> list[str]:
        chunks = []
        current_chunk = ""
        for paragraph in text.split(". "):
            if Tokenizer.count(current_chunk + paragraph) < MAX_TOKENS / 2:
                current_chunk += paragraph + ". "
            else:
                chunks.append(current_chunk)
                current_chunk = paragraph + ". "
        if current_chunk:
            chunks.append(current_chunk)
        for chunk in chunks:
            print(Tokenizer.count(chunk))
        return chunks