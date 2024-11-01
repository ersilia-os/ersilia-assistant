import os

from llama_index.embeddings.huggingface import HuggingFaceEmbedding

LLAMAFILE_URL = os.environ.get("llamafile_url")
BASE_URL = LLAMAFILE_URL
EMBEDDING = HuggingFaceEmbedding("BAAI/bge-base-en-v1.5")

EOF_TOKEN = "<|eot_id|>"
REWRITE = "Rewrite"

STOP_TOKENS = [  #OpenAI Chat API only allows for upto four such tokens
    EOF_TOKEN
]

