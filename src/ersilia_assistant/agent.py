from typing import Dict, List
from pydantic import BaseModel
from .model_selector import ModelSelector
from .recipe_generator import RecipeGenerator
from .summarizer_engine import Summarizer
from .util import llm_filter
from .defaults import QUERY_REJECTION_TEXT, LINE_BREAK


class ErsiliaAssistant:
    def __init__(self) -> None:
        self.model_selector = ModelSelector()
        self.recipe_generator = RecipeGenerator()
        self.summarizer = Summarizer()
        self.summary = None
        self.models = []

    def pipeline(self, query: str):
        for token in self.summarizer.summarize(query):
            yield token

        yield LINE_BREAK

        # Stream model selection response
        for token in self.model_selector.select_models(query):
            yield token

        yield LINE_BREAK

        # Stream recipe response
        for token in self.recipe_generator.generate(
            self.model_selector.selected_models
        ):
            yield token

    def run(self, query: str):
        relevant_query = llm_filter(query)
        if not relevant_query:
            for word in QUERY_REJECTION_TEXT.split(sep=" "):
                yield word + " "
        else:
            for token in self.pipeline(query):
                yield token
