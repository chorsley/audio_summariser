"""
Values shared across the project.
"""

from os import environ
import sys

MAX_TOKENS = {
    "gpt-4": 8000,
    "gpt-3.5-turbo": 4000
}

try:
    OPENAI_API_KEY = environ["OPENAI_API_KEY"]
except KeyError:
    print("Please set the OPENAI_API_KEY environment variable.")
    sys.exit(1)
