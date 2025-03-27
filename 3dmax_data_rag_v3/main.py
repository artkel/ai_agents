from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os, getpass, pprint
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_cohere import CohereEmbeddings
from langchain_chroma import Chroma
from custom_splitter import ChapterAwareMaxSplitter

# Load environment variables
load_dotenv()

# Get API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")


llm = init_chat_model("gpt-4o-mini", model_provider="openai")

# embed-multilingual-v3.0 - 1024 dimensions, max 512 tokens
# text-embedding-3-large - 3072 dimensions, max input 8191
cohere_embeddings = CohereEmbeddings(
        model="embed-multilingual-v3.0", # text-embedding-3-large // open ai
        cohere_api_key=COHERE_API_KEY
)


file_path = "./data/3dmax_data.pdf"
loader = PyPDFLoader(file_path)
documents = loader.load()

# print(f"Loaded {len(documents)} document pages.")

splitter = ChapterAwareMaxSplitter()

chunks = splitter.split_documents(documents)
# print(f"Split into {len(chunks)} chunks.")

# Create a Chroma vector store from our documents using Cohere embeddings
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=cohere_embeddings,
    persist_directory="./chroma_db"  # Store the database locally
)

print(f"Created and persisted Chroma vector database at './chroma_db'")

# Test a simple retrieval to make sure it's working
test_query = "Как выбрать систему координат?"
results = vectorstore.similarity_search(test_query, k=1)  # Get top the most similar chunk

print(f"\nTest retrieval for query: '{test_query}'")
print(f"Found {len(results)} relevant chunks.")

# Display the results
for i, doc in enumerate(results):
    print(f"\nResult {i+1}:")
    print(f"Source: Page {doc.metadata.get('page', 'unknown')}")
    print(f"Content preview: {doc.page_content[:250]}...")