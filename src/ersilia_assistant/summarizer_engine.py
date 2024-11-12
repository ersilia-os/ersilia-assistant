from typing import List


from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core import PromptTemplate
from llama_index.llms.llamafile import Llamafile

from .defaults import LLAMA_SERVER, STOP_TOKENS, REQUEST_TIMEOUT


class Summarizer:
    def __init__(self) -> None:

        self.llm = Llamafile(base_url=LLAMA_SERVER, request_timeout=REQUEST_TIMEOUT)
        self.response_header = """
        This is my understanding of your query:
        """

        self.response_format = f"""
        When generating a response you should separate each line by a newline character and use numerical bullets.
        Each line should be in second person.
        Always begin your response with the following line:
        {self.response_header}
        """

        self.sample_prompts = {
            1: {
                "query": "What is the molecular weight of aspirin?",
                "response": "This is my understanding of your query:\n1. You are interested in the molecular weight of aspirin.",
            },
            2: {
                "query": "I am working on a drug discovery project for malaria. I am interested in compounds active in the sexual and asexual stages of the parasite. I want some good starting points with new mechanisms of action.",
                "response": "This is my understanding of your query:\n1. You are working on a drug discovery project for malaria.\n2. You are interested in compounds active in the sexual and asexual stages of the parasite.\n3. You want some good starting points with new mechanisms of action.",
            },
        }

        self.examples = "\n".join(
            [
                f"- {v['query']}\n You should respond with: {v['response']}"
                for k, v in self.sample_prompts.items()
            ]
        )

        self.prompt_template_base = f"""
        You are a biomedical and a drug discovery expert responding to a user query.
        Your need to comprehend and interpret user query and divide it into bullet points.
        Bullet points should be concise, not ambiguous, and contain only one concept.
        Do not make assumptions about the user's background.
        Here are a few examples of queries that you can expect:
        {self.examples}
        Also, bullet points should be logically ordered, if possible.
        """
        self.summary_prompt_template_str = (
            self.prompt_template_base
            + """
        Query: {query}
        """
        )
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
