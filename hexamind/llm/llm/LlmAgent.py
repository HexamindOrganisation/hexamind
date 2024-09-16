import os
import logging
from hexamind.llm.adapters.AbstractLlm import ILlmClient
from hexamind.utils.llm.template import Template
from transformers import AutoTokenizer, AutoModelForMaskedLM
import torch

logger = logging.getLogger(__name__)


class LlmAgent:
    def __init__(self, client: ILlmClient):
        logger.info(f"Initializing LlmAgent with client type: {type(client)}")
        if not isinstance(client, ILlmClient):
            logger.error("Client should be an instance of ILlmClient")
            raise TypeError("client should be an instance of ILlmClient")

        self.client = client
        self.sparse_tokenizer = AutoTokenizer.from_pretrained(
            "naver/splade-cocondenser-ensembledistil"
        )
        self.sparse_model = AutoModelForMaskedLM.from_pretrained(
            "naver/splade-cocondenser-ensembledistil"
        )

    def send_request_to_llm(self, messages):
        return self.client.chat(messages=messages)

    def generate_paragraph(
        self,
        query: str,
        context: dict,
        histo: list[(str, str)],
        glossary: str,
        language: str = "fr",
    ) -> str:
        template = Template.generate_paragraph(
            query, context, histo, glossary=glossary, language=language
        )
        logger.debug(f"Generated paragraph template: {template}")
        messages = [self.client.create_chat_message("user", template)]
        response = self.send_request_to_llm(messages)
        return str(response)

    def translate(self, text: str) -> str:
        template = Template.translate(text)
        messages = [self.client.create_chat_message("user", template)]
        response = self.send_request_to_llm(messages)
        return str(response)

    def generate_answer(
        self, query: str, answer: str, histo: str, context: str, language: str
    ) -> str:
        template = Template.generate_answer(query, answer, histo, context, language)
        messages = [self.client.create_chat_message("user", template)]
        response = self.send_request_to_llm(messages)
        return str(response)

    def summarize(self, text: str, title_doc: str = "", title_para: str = ""):
        template = Template.summarize_paragraph(text, title_doc, title_para)
        logger.debug(f"Generated summarize template: {template}")
        messages = [self.client.create_chat_message("user", template)]
        response = self.send_request_to_llm(messages)
        logger.debug(f"Summarize response: {response}")
        return str(response)

    def detect_language(self, text: str) -> str:
        template = Template.detect_language(text)
        messages = [self.client.create_chat_message("user", template)]
        response = self.send_request_to_llm(messages)
        return str(response)

    def get_embedding(self, text):
        embeddings_batch_response = self.client.embeddings(input=[text])
        return embeddings_batch_response.data[0].embedding

    def get_sparse_embedding(self, text):
        inputs = self.sparse_tokenizer(
            text, return_tensors="pt", truncation=True, max_length=512
        )
        with torch.no_grad():
            outputs = self.sparse_model(**inputs)
            sparse_vector = (
                torch.max(
                    torch.log(1 + torch.relu(outputs.logits))
                    * inputs.attention_mask.unsqueeze(-1),
                    dim=1,
                )[0]
                .squeeze()
                .tolist()
            )

        return sparse_vector

    @staticmethod
    def print_response(self, response):
        logger.info("****************")
        logger.info(response)
        logger.info("----")
