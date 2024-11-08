import os
from typing import Dict, List, Generator

from openai import OpenAI

from .index.models import ErsiliaModelMetadataIndex
from .defaults import FILTER_TOKENS, STOP_TOKENS, LLAMAFILE_URL

DATA_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "data")
PUBLICATIONS_DIR = os.path.join(DATA_DIR, "publications")

class ModelSelector:
    def __init__(self) -> None:
        self.index = ErsiliaModelMetadataIndex()
        self.query_engine = self.index.query_engine(streaming=True)
        self.prepend_text = "For your query, I have selected the following models:"

    def _get_model_title(self, node) -> str:
        return node.to_dict()["node"]["text"]["title"]
    
    def _get_model_interpretation(self, node) -> str:
        return node.to_dict()["node"]["text"]["interpretation"]
    
    def _get_publication_summary(self, model, node) -> str:

        file_path = os.path.join(PUBLICATIONS_DIR, f"{model}.json")
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                summary = f.read()
        else:
            summary = self._get_model_interpretation(node)

        return summary
            
    def _get_model_reason(self, query: str, summary: str) -> Generator[str, None, None]:
        sys_prompt = f"""
        You are a helpful assistant who can explain why a given model is best suited to the task, based on the context.
        Given this context, explain why the model is best suited to the task.
        Context: {summary}\n
        """
        client = OpenAI(
            base_url=f"{LLAMAFILE_URL}/v1",
            api_key="sk-no-key-required",
        )

        completion = client.chat.completions.create(
            model="LLaMA_CPP",
            messages=[
                {
                    'role': 'system',
                    'content': sys_prompt
                },
                {
                    'role': 'user',
                    'content': query     
                }
            ],
            stream=True,
            stop=STOP_TOKENS
        )
        for chunk in completion:
            yield chunk.choices[0].delta.content

    def _get_model_url(self, model) -> str:
        return f"https://github.com/ersilia-os/{model}"
    
    def get_models(self, query: str) -> List[str]:
        retrieved_nodes = self.index.retrieve(query)
        model_ids = self.index.nodes_to_model_ids(retrieved_nodes)
        return retrieved_nodes, model_ids

    def select_models(self, retrieved_nodes, model_ids) -> Generator[str, None, None]:
        for word in self.prepend_text.split(sep=" "):
            yield word + " "

        for model in model_ids:
            node = retrieved_nodes[model_ids.index(model)]
            url = self._get_model_url(model)
            title = self._get_model_title(node=node)
            yield model+"\n"
            yield "*URL*: " + url + "\n"
            yield "*Title*: " + title + "\n"
            yield "*Explanation*: " + "\n"
            for word in self._get_publication_summary(model, node):
                yield word + " "

    def query_llm_for_models(
        self, query: str
    ) -> Generator[str, None, None]:
        response = self.query_engine.query(query)
        for token in response.response_gen:
            if token not in FILTER_TOKENS:
                yield token
