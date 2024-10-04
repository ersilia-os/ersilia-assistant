import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

from ersilia_assistant.defaults import EMBEDDING, LLM

#TODO Clean this up
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../.."))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
DISEASE_DIR = os.path.join(DATA_DIR, 'diseases')

#TODO Maybe this can become a base class for all the indexes
class ErsiliaDiseaseIndex:
    def __init__(self) -> None:
        documents = SimpleDirectoryReader(DISEASE_DIR).load_data()
        #TODO this is ugly, can we subclass VectorStoreIndex?
        self.index = VectorStoreIndex.from_documents(documents, embed_model=EMBEDDING)
        self.llm = LLM
    def query_engine(self):
        return self.index.as_query_engine(llm=self.llm)
    
    def load_index(self):
        pass

    def persist_index(self):
        pass
