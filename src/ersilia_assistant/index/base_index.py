import os

from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)
from llama_index.llms.llamafile import Llamafile
from ..defaults import EMBEDDING, LLAMA_SERVER, REQUEST_TIMEOUT


class BaseErsiliaIndex:

    def __init__(self, data_dir: str) -> None:
        self.llm = Llamafile(base_url=LLAMA_SERVER, request_timeout=REQUEST_TIMEOUT)
        self.store_path = f"{data_dir}/store"
        self.data_dir = data_dir

        if os.path.exists(self.store_path):
            self.index = self.load_index()

        else:
            self.index = self.create_index(data_dir=data_dir)
            self.persist_index()

    def query_engine(self):
        raise NotImplementedError()

    def create_index(self, data_dir: str):
        # This should be run if no index exists already.
        # It may happen that the package data ends up in an environment that's 'hidden'
        # So we set exclude_hidden=False to ensure metadata discoverability
        documents = SimpleDirectoryReader(data_dir, exclude_hidden=False).load_data()
        return VectorStoreIndex.from_documents(documents, embed_model=EMBEDDING)

    def load_index(self):
        storage_context = StorageContext.from_defaults(persist_dir=self.store_path)
        return load_index_from_storage(
            storage_context=storage_context, embed_model=EMBEDDING
        )

    def persist_index(self):
        self.index.storage_context.persist(persist_dir=self.store_path)
