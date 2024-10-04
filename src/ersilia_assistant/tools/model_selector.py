from typing import List

from llama_index.core import PromptTemplate

from ersilia_assistant.defaults import BASE_URL, LLM
from ersilia_assistant.indexes import ErsiliaModelMetadataIndex

class ModelSelector:
    def __init__(self) -> None:
        self.query_engine = ErsiliaModelMetadataIndex().query_engine()
    
    def select_models(self, query: str) -> List[str]:
        response = self.query_engine.query(query)
        return response

if __name__ == '__main__':
    model_selector = ModelSelector()
    with open("ersilia-assistant/experiments/prompts.txt", "r") as fp:
        queries = fp.readlines()
    
    queries = list(filter(lambda x: x.strip() != "", queries))
    
    for query in queries:
        print("User query: ", query)
        query = "I want model identifiers corresponding to the following query: " + query
        models = model_selector.select_models(query)
        print("Model response: ", models)
        print("\n=========================================================\n")
        
