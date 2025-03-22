from langchain_community.document_loaders import PyPDFLoader
import os, getpass
from langchain.chat_models import init_chat_model
from langchain_cohere import CohereEmbeddings
from langchain_chroma import Chroma

if not os.environ.get("OPENAI_API_KEY"):
  os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")

if not os.environ.get("COHERE_API_KEY"):
  os.environ["COHERE_API_KEY"] = getpass.getpass("Enter API key for Cohere: ")

llm = init_chat_model("gpt-4o-mini", model_provider="openai")
embeddings = CohereEmbeddings(model="embed-multilingual-v3.0") # text-embedding-3-large // open ai

# embedding_model = "embed-multilingual-v3.0"