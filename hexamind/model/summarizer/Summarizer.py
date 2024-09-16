from typing import Optional, Dict, Any
from hexamind.llm.llm import LlmAgent


class Summarizer:
    def __init__(self, llm_agent: LlmAgent):
        self.llm_agent = llm_agent

    def summarize(self, text: str, doc_name: str, section_name: str) -> str:
        """Summarize the text"""
        return self.llm_agent.summarize(text, doc_name, section_name)
