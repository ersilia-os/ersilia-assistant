from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.llamafile import Llamafile

BASE_URL = "http://127.0.0.1:8080"
EMBEDDING = HuggingFaceEmbedding("BAAI/bge-base-en-v1.5")
LLM = Llamafile(base_url=BASE_URL)