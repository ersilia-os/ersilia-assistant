import os
from .base_index import BaseErsiliaIndex

from llama_index.core import QueryBundle
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.postprocessor import LLMRerank

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", "data"))
METADATA_DIR = os.path.join(DATA_DIR, "models")


class ErsiliaModelMetadataIndex(BaseErsiliaIndex):
    def __init__(self) -> None:
        super().__init__(METADATA_DIR)
        self.llm.system_prompt = """
        You are a helpful assistant who can select the best models from the context for the task.
        Select all relevant model identifiers from the context.
        """
        self.retriever = VectorIndexRetriever(index=self.index, similarity_top_k=10)
        self.llm_reranker = LLMRerank(llm=self.llm, top_n=10)

    def retrieve(self, query: str, with_reranker: bool = False):
        """The vector store index as a node retriever

        Parameters
        ----------
        query : str
            User query
        """
        query_bundle = QueryBundle(query)
        retrieved_nodes = self.retriever.retrieve(query_bundle)
        if with_reranker:
            retrieved_nodes = self.llm_reranker.postprocess_nodes(
                retrieved_nodes, query_bundle=query_bundle
            )
        return retrieved_nodes

    def nodes_to_model_ids(self, nodes):
        """Convert nodes to model ids

        Parameters
        ----------
        nodes : List
            List of nodes

        Returns
        -------
        List
            List of model ids
        """
        return [
            node.to_dict()["node"]["metadata"]["file_name"].strip(".json")
            for node in nodes
        ]

    def query_engine(self, top_k=10, streaming=True):
        """The vector store index as a query engine

        Parameters
        ----------
        top_k : int, optional
            Top K nodes to retrieve from the index, by default 10
        streaming : bool, optional
            Stream the output, by default True

        Returns
        -------
        Generator
            The LLM generated response based on the query and top_k nodes from the index.
        """
        if not top_k:
            return self.index.as_query_engine(llm=self.llm, streaming=streaming)
        else:
            return self.index.as_query_engine(
                llm=self.llm, similarity_top_k=top_k, streaming=streaming
            )
