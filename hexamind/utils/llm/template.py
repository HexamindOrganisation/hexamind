class Template:
    """
    Class template for the LLM agent.
    """

    @staticmethod
    def generate_paragraph(
        query: str, context: dict, histo: list[(str, str)], glossary: str, language: str
    ) -> str:
        """generates the  answer"""

        template = (
            f"You are a conversation bot designed to answer to the query from users.\n"
            f"You must answer the query using these context sources informations \n"
            f"-----\n"
            f"{context}\n"
            f"-----\n"
            f"Here is the query to answer : {query} in french\n"
            f"You are consistent and avoid redundancies with the rest of the initial conversation delimited by triple backticks :\n ``` {histo} ```\n"
            f"To help you answer the query, you can use the glossary information : \n"
            f"*****\n"
            f"{glossary}\n"
            f"*****\n"
            f"Your response shall be in {language} and shall be concise."
        )
        return template

    @staticmethod
    def translate(text: str) -> str:
        """translates"""

        template = f"Translate in english the text. If it is already in english, just return the text."
        return template

    @staticmethod
    def generate_answer(
        query: str, answer: str, histo: str, context: str, language=str
    ) -> str:
        """provides the final answer in {language} based on the initial query and the answer in english"""

        template = (
            f"Your task consists in translating the answer in {language}, if its not already the case, to the query "
            f"delimited by triple backticks: ```{query}``` \n"
            f"You don't add new content to the answer but: "
            f"1 You can use some vocabulary from the context delimited by triple backticks:\n"
            f"```{context}```\n"
            f"2 You are consistent and avoid redundancies with the rest of the initial"
            f"conversation delimited by triple backticks: ```{histo}```\n"
            f"Your response shall respect the following format:<response>\n"
            f"Here is the answer you are given in {language}:"
            f"{answer}"
        )
        return template

    @staticmethod
    def summarize_paragraph(prompt, title_doc, title_para):
        """
        summarizes the paragraph
        prompt: block content
        title_doc:
        title_para:
        """
        MAX_TOKENS = 850
        template = (
            f"Your task consists in summarizing in English the paragraph of the document untitled ```{title_doc}.``` located in the ```{title_para}``` section of the document."
            f"Your response shall be concise and shall respect the following format:"
            f"<summary>"
            f"If you see that the summary that you are creating will not respect ```{MAX_TOKENS}``` tokens, find a way to make it shorter."
            f"The paragraph you need to summarize is the following: {prompt}"
        )
        return template

    @staticmethod
    def detect_language(text):
        """detects the language of the text"""

        template = (
            f"Your task consists in detecting the language of the last question or sentence of the text."
            f"You should only give the two letters code of the language detected, nothing else."
        )
        return template
