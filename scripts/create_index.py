from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding


load_dotenv()

VectorStoreIndex.from_documents(
    SimpleDirectoryReader("./documents").load_data(True),
    show_progress=True,
    embed_model=GoogleGenAIEmbedding(),
).storage_context.persist("./app/index")
