from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.llamafile import Llamafile

BASE_URL = "http://127.0.0.1:8080"

documents = SimpleDirectoryReader("data").load_data()

Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")

# llamafile
Settings.llm = Llamafile(base_url=BASE_URL)

index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()
response = query_engine.query("What is this data about?")
print(response)