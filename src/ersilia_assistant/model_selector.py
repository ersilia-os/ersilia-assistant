from typing import Generator

from .metadata_engine import ErsiliaModelMetadataIndex
from .defaults import EOF_TOKEN

class ModelSelector:
    def __init__(self) -> None:
        self.query_engine = ErsiliaModelMetadataIndex().query_engine(streaming=True)

    def select_models(self, query: str) -> Generator[str, None, None]:  # TODO Add return type
        response = self.query_engine.query(query)
        for token in response.response_gen:
            if token != EOF_TOKEN:
                yield token
            
