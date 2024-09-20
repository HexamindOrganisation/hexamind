from pydantic import BaseModel, Field
import os

class IngestorConfig(BaseModel):
    chunking_strategy: str = Field(default="semantic", description="chunking strategy: semantic, block, level, section_number")
    max_tokens_per_chunk: int = Field(default=500, description="Maximum number of token per chunks")
    semantic_chunking_threshold: float = Field(default=0.5, description="Semantic chunking threshold")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"