import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.llamafile import Llamafile

from .defaults import EMBEDDING, BASE_URL

# TODO Clean this up
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../..", "data"))
DISEASE_DIR = os.path.join(DATA_DIR, "diseases")


# TODO Maybe this can become a base class for all the indexes
class ErsiliaDiseaseIndex:
    def __init__(self) -> None:
        documents = SimpleDirectoryReader(DISEASE_DIR).load_data()
        # TODO this is ugly, can we subclass VectorStoreIndex?
        self.index = VectorStoreIndex.from_documents(documents, embed_model=EMBEDDING)
        self.llm = Llamafile(base_url=BASE_URL)

    def query_engine(self, streaming=True):
        return self.index.as_query_engine(llm=self.llm, streaming=streaming)

    def load_index(self):
        pass

    def persist_index(self):
        pass
