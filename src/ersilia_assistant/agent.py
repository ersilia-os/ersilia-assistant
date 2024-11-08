from typing import Dict, List
from pydantic import BaseModel
from .model_selector import ModelSelector
from .recipe_generator import RecipeGenerator
from .summarizer_engine import Summarizer
from .util import query_filter
from .defaults import QUERY_REJECTION_TEXT

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

        # Get models
        nodes, ids = self.model_selector.get_models(query)

        # Stream model response
        for token in self.model_selector.select_models(nodes, ids):
            yield token

        # Stream recipe response
        for token in self.recipe_generator.generate(ids):
            yield token

    def run(self, query: str):
        relevant_query = query_filter(query)
        if not relevant_query:
            for word in QUERY_REJECTION_TEXT.split(sep=" "):
                yield word + " "
        else:
            for token in self.pipeline(query):
                yield token
