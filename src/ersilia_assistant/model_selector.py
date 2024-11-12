import os
import json
from typing import List, Generator

from openai import OpenAI

from .index.models import ErsiliaModelMetadataIndex
from .defaults import FILTER_TOKENS, STOP_TOKENS, LLAMA_SERVER, LINE_BREAK
from .util import llm_filter

DATA_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "data")
PUBLICATIONS_DIR = os.path.join(DATA_DIR, "publications")


class ModelSelector:
    def __init__(self) -> None:
        self.index = ErsiliaModelMetadataIndex()
        self.query_engine = self.index.query_engine(streaming=True)
        self.prepend_text_multiple = "For your query, I have selected the following models:"
        self.prepend_text_singular = "For your query, I have selected the following model:"
        self.prepend_text_none = "I could not find any models that are relevant to your query."
        self.model_filter_prompt = """
        You are a helpful assistant who is an expert in biomedicine.
        Given a query, and a context you can determine if the context is relevant to the query.
        Only use information from the context and nothing else.
        Respond with either True or False.
        Context: {context}
        Query: {query}
        """
        self.selected_models = []
        self.selected_nodes = []

    def _get_model_title(self, node) -> str:
        text = node.to_dict()["node"]["text"]
        metadata = json.loads(text)
        return metadata["Title"]

    def _get_model_interpretation(self, node) -> str:
        text = node.to_dict()["node"]["text"]
        metadata = json.loads(text)
        return metadata["Interpretation"]

    def _get_publication_summary(self, model, node) -> str:
        file_path = os.path.join(PUBLICATIONS_DIR, f"{model}.json")
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                summary = f.read()
        else:
            summary = self._get_model_interpretation(node)

        return summary

    def _check_model_relevance(self, query: str, summary: str) -> bool:
        system_prompt = self.model_filter_prompt.format(context=summary, query=query)
        relevance = llm_filter(query, system_prompt)
        return relevance

    def _get_model_reason(self, query: str, summary: str) -> Generator[str, None, None]:
        sys_prompt = f"""
        You are a helpful assistant who can explain why a given model is best suited to the task, based on the context.
        Given this context, explain why the model is best suited to the task.
        Keep the explaination concise and to the point.
        Do not include any irrelevant information that is not present in the context.
        Keep the word limit to 200 words.
        Context: {summary}\n
        """
        client = OpenAI(
            base_url=f"{LLAMA_SERVER}/v1",
            api_key="sk-no-key-required",
        )

        completion = client.chat.completions.create(
            model="LLaMA_CPP",
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": query},
            ],
            stream=True,
            stop=STOP_TOKENS,
        )
        for chunk in completion:
            yield chunk.choices[0].delta.content

    def _get_model_url(self, model) -> str:
        return f"https://github.com/ersilia-os/{model}"

    def _select_models(self, query: str) -> List[str]:
        retrieved_nodes = self.index.retrieve(query)
        model_ids = self.index.nodes_to_model_ids(retrieved_nodes)

        # Filter nodes based on model relevance to query
        # using the model's publication summary
        selected_nodes = list(
            filter(
                lambda node: self._check_model_relevance(
                    query,
                    self._get_publication_summary(
                        model_ids[retrieved_nodes.index(node)], node
                    ),
                ),
                retrieved_nodes,
            )
        )

        # Keep only the model ids of the filtered nodes
        selected_models = list()
        for node in selected_nodes:
            selected_models.append(model_ids[retrieved_nodes.index(node)])

        self.selected_models = selected_models
        self.selected_nodes = selected_nodes

    def select_models(self, query) -> Generator[str, None, None]:
        self._select_models(query)

        # TODO: Sorry this is very ugly, and we should do away with hardcoding this.
        beginning_text = self.prepend_text_multiple if len(self.selected_models) > 1 else (
            self.prepend_text_singular if len(self.selected_models) == 1 else self.prepend_text_none
        )
        for word in beginning_text.split(sep=" "):
            yield word + " "
        yield LINE_BREAK

        for model in self.selected_models:
            node = self.selected_nodes[self.selected_models.index(model)]
            summary = self._get_publication_summary(model, node)
            url = self._get_model_url(model)
            title = self._get_model_title(node=node)
            yield f"**Model**: {model}" + LINE_BREAK
            yield "**URL**: " + url + LINE_BREAK
            yield "**Title**: " + title.title() + LINE_BREAK
            yield "**Explanation**: " + LINE_BREAK
            for token in self._get_model_reason(query, summary):
                if token:
                    yield token + " "
            yield LINE_BREAK*2

    def query_llm_for_models(self, query: str) -> Generator[str, None, None]:
        response = self.query_engine.query(query)
        for token in response.response_gen:
            if token not in FILTER_TOKENS:
                yield token
