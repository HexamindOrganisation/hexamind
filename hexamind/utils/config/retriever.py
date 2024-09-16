from pydantic import BaseModel, Field
import os

class RetrieverConfig(BaseModel):
    cohere_api_key: str = Field(default=os.getenv("COHERE_API_KEY"), description="API key for Cohere")
    max_hybrid_search_results: int = Field(default=50, description="Maximum number of results to return from hybrid search")
    rrf_k: int = Field(default=60, description="RRF constant for hybrid search")
    rerank_model: str = Field(default="rerank-multilingual-v3.0", description="Model to use for reranking")
    max_rerank_results: int = Field(default=30, description="Maximum number of results to return from reranking")
    peloton_alpha: float = Field(default=0.15, description="Alpha parameter for peloton selection")
    peloton_beta: float = Field(default=0.3, description="Beta parameter for peloton selection")
    min_chunks_to_return: int = Field(default=0, description="Minimum number of chunks to return")
    max_chunks_to_return: int = Field(default=8, description="Maximum number of chunks to return")
    relevance_threshold: float = Field(default=0.05, description="Minimum relevance score for a chunk to be considered relevant")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"