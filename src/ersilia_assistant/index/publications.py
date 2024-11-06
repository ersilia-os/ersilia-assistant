import os
from .base_index import BaseErsiliaIndex

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", "data"))
PUBLICATION_DIR = os.path.join(DATA_DIR, "publications")


class ErsiliaModelPublicationIndex(BaseErsiliaIndex):
    def __init__(self) -> None:
        super().__init__(PUBLICATION_DIR)

    def query_engine(self, top_k=10, streaming=True):
        # TODO
        raise NotImplementedError()
