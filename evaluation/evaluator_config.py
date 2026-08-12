from google import genai

from ragas.llms import llm_factory
from ragas.embeddings import GoogleEmbeddings

from utils.config import settings


def get_evaluator_llm():

    client = genai.Client(
        api_key=settings.gemini_api_key
    )

    return llm_factory(
        settings.model_name,
        provider="google",
        client=client
    )


def get_evaluator_embeddings():

    client = genai.Client(
        api_key=settings.gemini_api_key
    )

    return GoogleEmbeddings(
        client=client,
        model="gemini-embedding-001"
    )