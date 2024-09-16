from typing import List
from mistral_common.protocol.instruct.request import ChatCompletionRequest
from mistral_common.protocol.instruct.messages import UserMessage
from mistral_common.tokens.tokenizers.mistral import MistralTokenizer
from hexamind.model.chunk.itokenizer import ITokenizer


class Tokenizer(ITokenizer):

    def __init__(self):
        self.tokenizer = MistralTokenizer.from_model("open-mixtral-8x22b")

    def tokenize(self, text: str) -> List[int]:
        request = ChatCompletionRequest(messages=[UserMessage(content=text)])
        tokenized = self.tokenizer.encode_chat_completion(request)
        return tokenized.tokens

    def decode(self, tokens: List[int]) -> str:
        return self.tokenizer.decode(tokens)

    def count_tokens(self, text: str) -> int:
        return len(self.tokenize(text))
