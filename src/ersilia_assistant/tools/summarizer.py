from typing import List

from llama_index.core import PromptTemplate

from ersilia_assistant.defaults import BASE_URL, LLM
from ersilia_assistant.indexes import ErsiliaDiseaseIndex

class Summarizer:
    def __init__(self) -> None:
        self.summary_prompt_template_str = """
        You are a helpful assistant who can summarize what is being asked.
        Based on this instruction, generate a summary of what is asked, \
        one element on each line, related to the following input query:
        Query: {query}
        """
        self.summary_gen_prompt = PromptTemplate(self.summary_prompt_template_str)
        self.query_engine = ErsiliaDiseaseIndex().query_engine()
        self.llm = LLM
    
    def summarize_query_without_index(self, query: str) -> List[str]:
        response = self.llm.predict(self.summary_gen_prompt, query=query)
        summary = response.split("\n")
        # print(f"Generated Summary: \n{summary}")
        return summary

    def summarize_query_with_index(self, query: str) -> List[str]:
        response = self.query_engine.query(self.summary_gen_prompt, query=query)
        summary = response.split("\n")
        print(f"Generated Summary: \n{summary}")
        return summary


if __name__ == '__main__':
    summarizer = Summarizer()
    with open("ersilia-assistant/experiments/prompts.txt", "r") as fp:
        queries = fp.readlines()
    
    queries = list(filter(lambda x: x.strip() != "", queries))
    
    for query in queries:
        print("User query: ", query)
        summary = summarizer.summarize_query_without_index(query)
        print("Model response: ", summary[2:])
        print("\n=========================================================\n")

