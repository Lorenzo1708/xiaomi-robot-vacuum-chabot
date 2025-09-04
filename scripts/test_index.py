from dotenv import load_dotenv
from llama_index.core import load_index_from_storage, StorageContext
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.llms.google_genai import GoogleGenAI


load_dotenv()

print(
    load_index_from_storage(
        StorageContext.from_defaults(persist_dir="./app/index"),
        embed_model=GoogleGenAIEmbedding(),
    )
    .as_query_engine(GoogleGenAI("gemini-2.5-flash"), similarity_top_k=4)
    .query("Summarize the safety information.")
)
