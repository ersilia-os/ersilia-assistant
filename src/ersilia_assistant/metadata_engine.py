import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.llms.llamafile import Llamafile

from .defaults import EMBEDDING, BASE_URL


CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "data"))
METADATA_DIR = os.path.join(DATA_DIR, "models-metadata")


# TODO CustomQueryEngine?
class ErsiliaModelMetadataIndex:
    def __init__(self) -> None:
        self.llm = Llamafile(base_url=BASE_URL)
        self.llm.system_prompt = """
        You are a helpful assistant who can select the best models from the context for the task.
        Select all relevant model identifiers from the context.
        """

        # It may happen that the package data ends up in an environment that's 'hidden'
        # So we set exclude_hidden=False to ensure metadata discoverability
        documents = SimpleDirectoryReader(METADATA_DIR, exclude_hidden=False).load_data()
        self.index = VectorStoreIndex.from_documents(documents, embed_model=EMBEDDING)

    def query_engine(self, top_k=10, streaming=True):
        # This is ugly, we should use kwargs instead and add more customizations
        if not top_k:
            return self.index.as_query_engine(llm=self.llm, streaming=streaming)
        else:
            return self.index.as_query_engine(
                llm=self.llm, similarity_top_k=top_k, streaming=streaming
            )

    def load_index(self):
        # TODO This only creates a storage context, we need to load from persistent disk
        self.index.storage_context.from_defaults(persist_dir=METADATA_DIR)

    def persist_index(self):
        self.index.storage_context.persist(persist_dir=METADATA_DIR)
