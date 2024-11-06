import os
from .base_index import BaseErsiliaIndex

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", "data"))
DISEASE_DIR = os.path.join(DATA_DIR, "diseases")


class ErsiliaDiseaseIndex(BaseErsiliaIndex):
    def __init__(self) -> None:
        super().__init__(DISEASE_DIR)

    def query_engine(self, streaming=True):
        return self.index.as_query_engine(llm=self.llm, streaming=streaming)
