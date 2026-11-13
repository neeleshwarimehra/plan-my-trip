
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


GROQ_MODEL = os.getenv("GROQ_MODEL")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY is missing. Check your backend .env file."
    )


llm = ChatGroq(
    model=GROQ_MODEL,
    temperature=0,
    max_tokens=2000,
    api_key=GROQ_API_KEY,
)


def get_llm() -> ChatGroq:
    """Return the shared Groq chat model."""
    return llm
