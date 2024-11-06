import os

from llama_index.embeddings.huggingface import HuggingFaceEmbedding


LLAMAFILE_URL = os.environ.get("llamafile_url")
BASE_URL = LLAMAFILE_URL
REQUEST_TIMEOUT = os.environ.get("request_timeout", 30.0)  # Default for llamafile
EMBEDDING = HuggingFaceEmbedding("BAAI/bge-base-en-v1.5")

EOF_TOKEN = "<|eot_id|>"
REWRITE = "Rewrite"

STOP_TOKENS = [EOF_TOKEN]  # OpenAI Chat API only allows for upto four such tokens
FILTER_TOKENS = [EOF_TOKEN, REWRITE]