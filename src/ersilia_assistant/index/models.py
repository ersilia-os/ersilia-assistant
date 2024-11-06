import os
from .base_index import BaseErsiliaIndex

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..","data"))
METADATA_DIR = os.path.join(DATA_DIR, "models")


class ErsiliaModelMetadataIndex(BaseErsiliaIndex):
    def __init__(self) -> None:
        super().__init__(METADATA_DIR)
        self.llm.system_prompt = """
        You are a helpful assistant who can select the best models from the context for the task.
        Select all relevant model identifiers from the context.
        """

    def query_engine(self, top_k=10, streaming=True):
        if not top_k:
            return self.index.as_query_engine(llm=self.llm, streaming=streaming)
        else:
            return self.index.as_query_engine(
                llm=self.llm, similarity_top_k=top_k, streaming=streaming
            )

