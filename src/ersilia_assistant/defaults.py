from typing import Any
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

BASE_URL = "http://127.0.0.1:8080"
EMBEDDING = HuggingFaceEmbedding("BAAI/bge-base-en-v1.5")

EOF_TOKEN = "<|eot_id|>"

STOP_TOKENS = [  #OpenAI Chat API only allows for upto four such tokens
    EOF_TOKEN
]
        
