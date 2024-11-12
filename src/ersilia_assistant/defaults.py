import os

from llama_index.embeddings.huggingface import HuggingFaceEmbedding


LLAMA_SERVER = os.environ.get("llamafile_url", "http://127.0.0.1:8080")
REQUEST_TIMEOUT = os.environ.get("request_timeout", 30.0)  # Default for local llamafile server
EMBEDDING = HuggingFaceEmbedding("BAAI/bge-base-en-v1.5")

EOF_TOKEN = "<|eot_id|>"
REWRITE = "Rewrite"

STOP_TOKENS = [EOF_TOKEN]  # OpenAI Chat API only allows for upto four such tokens
FILTER_TOKENS = [EOF_TOKEN, REWRITE]

QUERY_REJECTION_TEXT = """I am sorry, I can only help with queries related to navigating the Ersilia Model Hub.
Please provide a query that is relevant to drug discovery experiments, for example:

- How to calculate molecular weight of aspirin?
- How can I predict the solubility of a compound?
"""

QUERY_RELEVANCE_FILTER_PROMPT = """
You are a helpful scientific assistant who can detect whether a user's query is relevant to a drug discovery experiment.
Here are a few examples of queries that you can expect:
- "What is the molecular weight of aspirin?"
- "I am working on a drug discovery project for malaria. I am interested in compounds active in the sexual and asexual stages of the parasite. I want some good starting points with new mechanisms of action."
- "I work on malaria drug discovery. We need compounds with a longer half-life so that they do not need to be given daily. They should be available orally. Can you propose analogues of my dataset? They should be active in animal models not only in vitro."
Based on the context, you should determine whether the query is relevant to a drug discovery experiment.
If the query is relevant, you should return True. Otherwise, you should return False.
"""

LINE_BREAK = "\n" * 3
