from typing import List


from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core import PromptTemplate
from llama_index.llms.llamafile import Llamafile

from .defaults import BASE_URL, STOP_TOKENS, REQUEST_TIMEOUT


class Summarizer:
    def __init__(self) -> None:

        self.llm = Llamafile(base_url=BASE_URL, request_timeout=REQUEST_TIMEOUT)
        self.response_header = """
        This is my understanding of your query:
        """

        self.response_format = f"""
        When generating a response you should separate each line by a newline character and use numerical bullets.
        Each line should be in second person.
        Always begin your response with the following line:
        {self.response_header}
        """

        self.summary_prompt_template_str = """
        You are a helpful assistant who can summarize what is being asked.
        Based on this instruction, generate a summary of what is asked, \
        one element on each line, related to the following input query:
        Query: {query}
        """
        self.system_message = ChatMessage(
            role=MessageRole.SYSTEM,
            content=self.response_format,
        )
        self.summary_gen_prompt = PromptTemplate(
            template=self.summary_prompt_template_str, prompt_type="summary"
        )

    def summarize(self, query: str):
        messages = [
            self.system_message,
            self.summary_gen_prompt.format_messages(query=query)[0],
        ]
        for chunk in self.llm.stream_chat(messages=messages, stop=STOP_TOKENS):
            # stream_chat returns a generator of ChatResponse objects
            # We need to yield the delta content of each response
            # Because the message content of each object has all the content
            # from the previous messages.
            yield chunk.delta
