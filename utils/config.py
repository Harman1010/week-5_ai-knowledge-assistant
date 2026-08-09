from pydantic_settings import BaseSettings , SettingsConfigDict

class Settings(BaseSettings):

    model_name : str = "gemini-2.5-flash"
    temperature : float = 0.0

    gemini_api_key : str

    top_k : int = 10
    rerank_top_k : int = 3

    embedding_model : str = "sentence-transformers/all-MiniLM-L6-v2"

    reranker_model : str = "cross-encoder/ms-marco-MiniLM-L6-v2"

    chunk_size : int = 1000
    chunk_overlap : int = 200

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()