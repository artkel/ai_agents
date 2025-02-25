from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.embeddings.bedrock import BedrockEmbeddings
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

def get_embedding_function():
    embeddings = OpenAIEmbeddings(
                model="text-embedding-3-large",
    )
    # embeddings = OllamaEmbeddings(model="nomic-embed-text")
    return embeddings