import os

from hexamind.llm.adapters.AbstractLlm import ILlmClient
from hexamind.utils.llm.template import Template


class LlmAgent:
    def __init__(self, client: ILlmClient):
        """ 
        Constructor for the LLM agent. 

        Attributes:
        client : ILlmClient
            The client to use for the LLM.
        
        Methods: 
        send_request_to_llm(self, messages)
            Send a request to the LLM and get the response.
        generate_paragraph(self, query, context, histo, language)
            Generate a paragraph based on the query, context, and history.
        translate(self, text)
            Translate the text to English.
        generate_answer(self, query, answer, histo, context, language)
            Generate an answer in the specified language based on the query and answer.
        summarize_paragraph(self, prompt, title_doc, title_para)
            Summarize the paragraph.
        detect_language(self, text)
            Detect the language of the text.
        """
        print("type: ", type(client), " DONE")
        if not isinstance(client, ILlmClient):  # TODO -> class not implemented yet
            raise TypeError("client should be an instance of ILlmClient")

        self.client = client

    def send_request_to_llm(self, messages):
        return self.client.chat(messages=messages)

    def generate_paragraph(
        self, query: str, context: dict, histo: list[(str, str)], language="fr"
    ) -> str:
        """generates the  answer"""
        template = Template.generate_paragraph(query, context, histo, language=language)
        messages = [self.client.create_chat_message("user", template)]
        response = self.send_request_to_llm(messages)
        return str(response)

    def translate(self, text: str) -> str:
        """translates"""
        template = Template.translate(text)
        messages = [self.client.create_chat_message("user", template)]
        response = self.send_request_to_llm(messages)
        return str(response)

    def generate_answer(
        self, query: str, answer: str, histo: str, context: str, language: str
    ) -> str:

        """provides the final answer in {language} based on the initial query and the answer in english"""
        template = Template.generate_answer(query, answer, histo, context, language)
        messages = [self.client.create_chat_message("user", template)]
        response = self.send_request_to_llm(messages)
        return str(response)

    def summarize(
        self, text: str, title_doc: str = "", title_para: str = ""
    ):
        
        """summarizes the paragraph"""
        template = Template.summarize_paragraph(
            text, title_doc, title_para
        )
        print("template \n", template)
        messages = [self.client.create_chat_message("user", template)]
        response = self.send_request_to_llm(messages)
        print("response\n", response)
        return str(response)

    def detect_language(self, text: str) -> str:

        """detects the language"""
        template = Template.detect_language(text)
        messages = [self.client.create_chat_message("user", template)]
        response = self.send_request_to_llm(messages)
        return str(response)

    def get_embedding(self, text):
        """
        Returns text sembeddings 
        """
        embeddings_batch_response = self.client.embeddings(input=[text])
        return embeddings_batch_response.data[0].embedding

    @staticmethod
    def print_response(self, response):
        print("****************")
        print(response)
        print("----")
