from typing import Generator

from .index.models import ErsiliaModelMetadataIndex
from .defaults import FILTER_TOKENS


class ModelSelector:
    def __init__(self) -> None:
        index = ErsiliaModelMetadataIndex()
        self.query_engine = index.query_engine(streaming=True)

    def select_models(
        self, query: str
    ) -> Generator[str, None, None]:
        response = self.query_engine.query(query)
        for token in response.response_gen:
            if token not in FILTER_TOKENS:
                yield token
