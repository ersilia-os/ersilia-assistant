import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, get_response_synthesizer
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor

from ersilia_assistant.defaults import EMBEDDING, LLM

#TODO Clean this up
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../.."))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
METADATA_DIR = os.path.join(DATA_DIR, 'models-metadata')

#TODO Maybe this can become a base class for all the indexes
class ErsiliaModelMetadataIndex:
    def __init__(self) -> None:
        documents = SimpleDirectoryReader(METADATA_DIR).load_data()
        #TODO this is ugly, can we subclass VectorStoreIndex?
        self.index = VectorStoreIndex.from_documents(documents, embed_model=EMBEDDING)
        self.llm = LLM

    def query_engine(self, top_k=10):
        # This is ugly, we should use kwargs instead and add more customizations
        if not top_k:
            return self.index.as_query_engine(llm=self.llm)
        else:
            return self.index.as_query_engine(llm=self.llm, similarity_top_k=top_k)

    def load_index(self):
        pass

    def persist_index(self):
        pass


