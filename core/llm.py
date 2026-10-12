import os

from langchain_mistralai import ChatMistralAI


def get_llm(temperature: float = 0.3) -> ChatMistralAI:
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError(
            "MISTRAL_API_KEY is not set. Add it to your .env file."
        )
    return ChatMistralAI(
        model="mistral-small-latest",
        mistral_api_key=api_key,
        temperature=temperature,
    )
