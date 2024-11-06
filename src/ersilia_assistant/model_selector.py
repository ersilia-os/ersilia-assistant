from typing import Generator

from .index.models import ErsiliaModelMetadataIndex
from .defaults import FILTER_TOKENS


class ModelSelector:
    def __init__(self) -> None:
        self.query_engine = ErsiliaModelMetadataIndex().query_engine(streaming=True)

    def select_models(
        self, query: str
    ) -> Generator[str, None, None]:  # TODO Add return type
        response = self.query_engine.query(query)
        for token in response.response_gen:
            if token not in FILTER_TOKENS:
                yield token
